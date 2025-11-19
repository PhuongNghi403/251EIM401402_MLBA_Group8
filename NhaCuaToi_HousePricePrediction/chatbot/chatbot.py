import os
from pypdf import PdfReader
import gradio as gr
import google.generativeai as genai

_API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or "AIzaSyDxOqoIkpsNfDfHzfoPtD1yV9BowsIu87o"
genai.configure(api_key=_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def load_pdf_knowledge(pdf_path="data/house_price_knowledge.pdf"):
    if not os.path.exists(pdf_path):
        print(f"[CẢNH BÁO] Không tìm thấy file: {pdf_path}")
        return "Không có tài liệu kiến thức (file PDF chưa được tải)."

    print(f"[INFO] Đang đọc file PDF: {pdf_path}")
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text += t + "\n"
    return text[:30000]


knowledge_text = load_pdf_knowledge()

system_prompt = f"""
Bạn là Trợ lý Tư vấn Giá Nhà cực kỳ am hiểu thị trường Việt Nam.
Trả lời chỉ dựa trên tài liệu dưới đây và kinh nghiệm thực tế.
Luôn nói tiếng Việt, ngắn gọn, thân thiện, chuyên nghiệp.

Nếu người dùng muốn nhận báo cáo → hỏi email nhẹ nhàng nhé!

TÀI LIỆU KIẾN THỨC:
{knowledge_text}
"""

def chat_with_bot(message, history):
    chat_history = ""
    for user_msg, bot_msg in history:
        chat_history += f"Người dùng: {user_msg}\nTrợ lý: {bot_msg}\n"

    prompt = f"{system_prompt}\n\nLịch sử:\n{chat_history}Người dùng: {message}\nTrợ lý:"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Bot đang hơi mệt, thử lại nhé ạ!\nLỗi: {str(e)[:100]}"


demo = gr.ChatInterface(
    fn=chat_with_bot,
    title="Trợ lý Tư vấn Giá Nhà",
    description="Hỏi gì cũng được về giá nhà, xu hướng, đầu tư...",
    examples=[
        "Giá nhà quận 7 hiện tại bao nhiêu?",
        "Có nên mua đất nền Bình Dương không?",
        "Yếu tố nào ảnh hưởng nhất đến giá nhà?",
        "Gửi em báo cáo giá nhà TP.HCM được không?"
    ],
    theme=gr.themes.Soft()
)

if __name__ == "__main__":
    print("Bot Tư vấn Giá Nhà")
    print(f"Đã tải kiến thức PDF: {len(knowledge_text):,} ký tự")
    _port = int(os.environ.get("CHATBOT_PORT", "7860"))
    _share = (os.environ.get("CHATBOT_SHARE", "false").lower() == "true")
    demo.launch(share=_share, server_name="127.0.0.1", server_port=_port)