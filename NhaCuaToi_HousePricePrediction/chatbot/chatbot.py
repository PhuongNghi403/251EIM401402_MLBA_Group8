import os
from pypdf import PdfReader
import gradio as gr
import google.generativeai as genai
import socket

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

def _find_free_port(preferred: int | None = None, extra_candidates: list[int] | None = None) -> int:
    candidates = []
    if preferred and preferred > 0:
        candidates.append(int(preferred))
    env_p = os.environ.get("GRADIO_SERVER_PORT") or os.environ.get("CHATBOT_PORT")
    try:
        env_p_i = int(env_p) if env_p else None
    except Exception:
        env_p_i = None
    if env_p_i and env_p_i not in candidates:
        candidates.append(env_p_i)
    if extra_candidates:
        for p in extra_candidates:
            if p not in candidates:
                candidates.append(int(p))
    if not candidates:
        candidates = list(range(7860, 7871))
    for p in candidates:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind(("127.0.0.1", int(p)))
            return int(p)
        except Exception:
            continue
        finally:
            try:
                s.close()
            except Exception:
                pass
    return 0

if __name__ == "__main__":
    print("Bot Tư vấn Giá Nhà")
    print(f"Đã tải kiến thức PDF: {len(knowledge_text):,} ký tự")
    env_port = os.environ.get("GRADIO_SERVER_PORT") or os.environ.get("CHATBOT_PORT")
    try:
        pref = int(env_port) if env_port else None
    except Exception:
        pref = None
    port = _find_free_port(preferred=pref, extra_candidates=list(range(7860, 7871)))
    share_flag = (os.environ.get("CHATBOT_SHARE", "false").lower() == "true")
    if port > 0:
        print(f"[INFO] Khởi chạy Gradio tại port {port}")
        demo.launch(share=share_flag, server_name="127.0.0.1", server_port=port)
    else:
        print("[WARN] Không tìm được port trống; để Gradio tự chọn.")
        demo.launch(share=share_flag, server_name="127.0.0.1")