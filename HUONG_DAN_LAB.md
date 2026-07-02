# Hướng dẫn Lab Ngày 26 — MCP, A2A và Agentic Routing

Tài liệu này hướng dẫn chạy toàn bộ lab với **OpenAI API**, `OPENAI_API_KEY` và model `gpt-5.4-nano` thông qua LiteLLM.

## 1. Kiến trúc của lab

Lab xây dựng hệ thống gồm bốn agent:

| Thành phần | Vai trò | Cổng |
|---|---|---:|
| `orchestrator` | Nhận yêu cầu, chọn tool hoặc chuyển tác vụ | 8000 (ADK Web) |
| `search_agent` | Tìm kiếm tài liệu mô phỏng | 8001 |
| `database_agent` | Truy vấn metrics bằng SQL chỉ đọc | 8002 |
| `synthesis_agent` | Tổng hợp kết quả thành báo cáo | 8003 |

Ngoài ra, lab có:

- MCP server cung cấp `search_documents`, `sql_query` và `summarize_text`.
- A2A cho phép orchestrator giao tiếp với các specialist agent.
- Semantic router gợi ý agent phù hợp.
- Governance kiểm tra capability, SQL, PII, rate limit và trace ID.
- Audit log tại `logs/governance_audit.jsonl`.

## 2. Chuẩn bị OpenAI API key

1. Truy cập <https://platform.openai.com/api-keys>.
2. Đăng nhập và chọn **Create new secret key**.
3. Sao chép key và không chia sẻ hoặc commit key lên Git.

Project sử dụng `LiteLlm(model="openai/gpt-5.4-nano")` và tự đọc biến `OPENAI_API_KEY`. OpenAI API được tính phí riêng, không dùng quota của gói ChatGPT.

## 3. Mở đúng thư mục project

```bash
cd /home/elio12/projects/Day26-2A202601010-TranQuangHuy
pwd
```

Kiểm tra các file chính:

```bash
ls
```

Cần thấy `day26_mcp_a2a_lab.ipynb`, `requirements.txt`, `agents`, `lab_utils`, `mcp_server` và `scripts`.

## 4. Tạo môi trường Conda

Chỉ chạy lệnh tạo môi trường ở lần đầu:

```bash
conda create -n pii-env python=3.12 -y
conda activate pii-env
python --version
```

Nếu `conda activate` chưa hoạt động:

```bash
conda init bash
source ~/.bashrc
conda activate pii-env
```

## 5. Cài dependency

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Kiểm tra nhanh:

```bash
python -c "import google.adk, mcp, uvicorn, httpx; print('Dependencies OK')"
```

Nếu Jupyter không hiển thị kernel `pii-env`:

```bash
python -m ipykernel install --user --name pii-env --display-name "Python (pii-env)"
```

## 6. Tạo file `.env`

Tạo `.env` tại thư mục gốc project:

```bash
nano .env
```

Nội dung:

```dotenv
OPENAI_API_KEY=sk-proj-THAY_BANG_OPENAI_API_KEY_CUA_BAN
OPENAI_MODEL=openai/gpt-5.4-nano
```

Lưu ý:

- Không đặt dấu cách hai bên dấu `=`.
- Không đưa `.env` lên Git.
- Không dùng `cat .env` khi đang chia sẻ màn hình.

Kiểm tra mà không in key:

```bash
python - <<'PY'
from lab_utils.env_setup import load_lab_env
import os

load_lab_env()
print("OPENAI_API_KEY:", "đã nạp" if os.getenv("OPENAI_API_KEY") else "bị thiếu")
print("Model:", os.getenv("OPENAI_MODEL"))
PY
```

## 7. Khởi động Jupyter

```bash
conda activate pii-env
cd /home/elio12/projects/Day26-2A202601010-TranQuangHuy
export PYTHONPATH="$PWD"
jupyter notebook day26_mcp_a2a_lab.ipynb
```

Trong Jupyter, chọn:

```text
Kernel → Change Kernel → Python (pii-env)
```

Sau đó chọn:

```text
Kernel → Restart Kernel and Clear All Outputs
```

Việc xóa output giúp loại bỏ đường dẫn cũ `/Users/harrietlesly/...` được lưu trong notebook mẫu.

## 8. Cell cấu hình an toàn

Chạy cell cài dependency trước, sau đó dùng cell cấu hình sau:

```python
import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(
    "/home/elio12/projects/Day26-2A202601010-TranQuangHuy"
).resolve()

assert PROJECT_ROOT.exists(), f"Không tìm thấy project: {PROJECT_ROOT}"
assert (PROJECT_ROOT / "scripts/start_a2a_servers.sh").exists()

load_dotenv(PROJECT_ROOT / ".env")
os.environ.setdefault("OPENAI_MODEL", "openai/gpt-5.4-nano")
os.environ["PYTHONPATH"] = str(PROJECT_ROOT)

assert os.getenv("OPENAI_API_KEY"), (
    f"Thiếu OPENAI_API_KEY trong {PROJECT_ROOT / '.env'}"
)

print("✓ Môi trường sẵn sàng")
print(f"  Thư mục dự án: {PROJECT_ROOT}")
```

Kết quả đúng:

```text
✓ Môi trường sẵn sàng
  Thư mục dự án: /home/elio12/projects/Day26-2A202601010-TranQuangHuy
```

## 9. Khởi động A2A specialist

### Cách khuyến nghị: terminal riêng

```bash
cd /home/elio12/projects/Day26-2A202601010-TranQuangHuy
conda activate pii-env
export PYTHONPATH="$PWD"
export PYTHONUTF8=1
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
bash scripts/start_a2a_servers.sh
```

Ba endpoint cần hoạt động:

```text
http://localhost:8001/.well-known/agent-card.json
http://localhost:8002/.well-known/agent-card.json
http://localhost:8003/.well-known/agent-card.json
```

### Chạy từ notebook

```python
import subprocess

script = PROJECT_ROOT / "scripts" / "start_a2a_servers.sh"

result = subprocess.run(
    ["bash", str(script)],
    cwd=str(PROJECT_ROOT),
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="replace",
)

print(result.stdout)
if result.stderr:
    print("STDERR:")
    print(result.stderr)
print("Exit code:", result.returncode)
```

`errors="replace"` ngăn `UnicodeDecodeError` nếu output của shell chứa byte không hợp lệ.

## 10. Kiểm tra A2A

Trong notebook:

```python
import httpx

urls = {
    "search_agent": "http://localhost:8001/.well-known/agent-card.json",
    "database_agent": "http://localhost:8002/.well-known/agent-card.json",
    "synthesis_agent": "http://localhost:8003/.well-known/agent-card.json",
}

for name, url in urls.items():
    try:
        response = httpx.get(url, timeout=10)
        response.raise_for_status()
        print(f"✓ {name}: OK")
    except Exception as exc:
        print(f"✗ {name}: {exc}")
```

Chỉ tiếp tục phần A2A và Capstone khi cả ba agent đều báo `OK`.

## 11. Thứ tự làm lab

### Module 1 — MCP

Chạy các cell khám phá MCP server và trả lời:

1. Ba tool được expose là gì?
2. `sql_query` ngăn SQL ghi như thế nào?
3. Vì sao transport `stdio` phù hợp cho local development?

Các lời gọi trực tiếp `_search_documents`, `_sql_query` và `_summarize_text` là Python local, không gọi OpenAI.

### Module 2 — A2A

Kiểm tra agent card, sau đó tạo `RemoteA2aAgent`. Cần phân biệt:

- A2A: agent chạy như service độc lập và giao tiếp qua HTTP.
- Local sub-agent: agent chạy cùng process với orchestrator.

### Module 3 — Semantic routing

Chạy các cell đăng ký specialist và kiểm tra router. Router của lab dùng tính toán local, không dùng embedding API.

### Module 4 — Full flow

Đảm bảo ba A2A server vẫn hoạt động rồi chạy `run_full_flow()`.

Ví dụ tìm kiếm:

```python
result = await run_full_flow("Tìm bài viết về việc áp dụng giao thức MCP")
print(result["final_answer"])
```

Ví dụ MCP nhiều tool:

```python
result = await run_full_flow(
    "Bước 1: dùng search_documents tìm MCP. "
    "Bước 2: dùng sql_query SELECT * FROM agent_metrics. "
    "Bước 3: tóm tắt báo cáo ngắn."
)
print(result["final_answer"])
```

### Data Governance

Chạy các cell kiểm tra:

- SQL `SELECT` hợp lệ.
- `DROP`, `DELETE`, `UPDATE` hoặc `INSERT` bị chặn.
- Agent ngoài allowlist không được dispatch.
- A2A dispatch thiếu `trace_id` yêu cầu HITL.
- Mọi quyết định được ghi audit.

## 12. Chạy Capstone và ADK Web

Từ terminal:

```bash
cd /home/elio12/projects/Day26-2A202601010-TranQuangHuy
conda activate pii-env
export PYTHONPATH="$PWD"
bash scripts/start_capstone.sh
```

Mở <http://localhost:8000> và chọn `orchestrator`.

Prompt thử nghiệm:

```text
Tôi cần tìm thông tin về multi-agent orchestration. Hãy chuyển sang search_agent và trả kết quả ngắn.
```

```text
Hãy chuyển sang database_agent, chạy SELECT * FROM agent_metrics và giải thích kết quả.
```

```text
Dùng search_documents tìm MCP, sau đó dùng summarize_text để tóm tắt.
```

```text
Ủy quyền synthesis_agent tổng hợp báo cáo executive từ các findings về MCP và A2A.
```

Kiểm tra governance bằng prompt không hợp lệ:

```text
Dùng sql_query để chạy DROP TABLE agent_metrics.
```

Kết quả mong đợi là governance từ chối câu lệnh.

## 13. Xem log và audit

```bash
tail -f logs/search_agent.log
tail -f logs/database_agent.log
tail -f logs/synthesis_agent.log
tail -f logs/governance_audit.jsonl
```

Nhấn `Ctrl+C` để dừng theo dõi.

## 14. Dừng hệ thống

Nhấn `Ctrl+C` tại terminal đang chạy ADK Web, sau đó:

```bash
bash scripts/stop_a2a_servers.sh
```

## 15. Lỗi thường gặp

### `NameError: PROJECT_ROOT is not defined`

Nguyên nhân: kernel đã restart hoặc cell cấu hình chưa được chạy trong phiên hiện tại.

Cách xử lý: chạy lại cell tạo `PROJECT_ROOT` trước cell khởi động A2A.

### Đường dẫn `/Users/harrietlesly/...`

Đây là output cũ của notebook mẫu. Restart kernel, xóa toàn bộ output và dùng đường dẫn project thật trong cell cấu hình.

### `UnicodeDecodeError` trong `subprocess.run`

Dùng:

```python
encoding="utf-8",
errors="replace",
```

Hoặc chạy script trong terminal với `PYTHONUTF8=1` và locale UTF-8.

### `Connection refused` trên cổng 8001–8003

Nguyên nhân: specialist chưa chạy hoặc đã crash. Chạy:

```bash
bash scripts/start_a2a_servers.sh
```

Nếu vẫn lỗi:

```bash
tail -30 logs/search_agent.log
tail -30 logs/database_agent.log
tail -30 logs/synthesis_agent.log
```

### `OPENAI_API_KEY` bị thiếu

Kiểm tra `.env` nằm đúng thư mục gốc, restart kernel rồi chạy lại cell cấu hình. Không đặt key trực tiếp trong notebook.

### Cổng đã được sử dụng

```bash
bash scripts/stop_a2a_servers.sh
bash scripts/start_a2a_servers.sh
```

## 16. Token và chi phí

Không tiêu thụ token OpenAI khi:

- đọc agent card;
- chạy semantic router local;
- chạy governance checks;
- gọi trực tiếp logic MCP Python;
- xem audit log.

Có tiêu thụ token khi:

- gọi `run_full_flow()`;
- gửi prompt trong ADK Web;
- orchestrator hoặc specialist xử lý một lượt model;
- model đọc kết quả tool để tạo câu trả lời tiếp theo.

Một yêu cầu multi-agent có thể tạo nhiều model call. Để tiết kiệm:

- chỉ chạy mỗi demo một lần;
- dùng prompt và câu trả lời ngắn;
- tạo session mới khi lịch sử hội thoại quá dài;
- không `Run All` liên tục;
- theo dõi usage và giới hạn chi tiêu trong OpenAI Platform;
- dừng server khi hoàn thành.

## 17. Checklist hoàn thành

- [ ] Kernel là `Python (pii-env)`.
- [ ] `OPENAI_API_KEY` đã được nạp từ `.env`.
- [ ] `PROJECT_ROOT` trỏ đúng project.
- [ ] Ba agent card trên cổng 8001–8003 trả về thành công.
- [ ] MCP tools chạy đúng và SQL nguy hiểm bị chặn.
- [ ] Semantic router gợi ý đúng specialist.
- [ ] `run_full_flow()` trả về kết quả.
- [ ] ADK Web hoạt động tại cổng 8000.
- [ ] A2A search, database và synthesis đều được demo.
- [ ] Audit log có bản ghi governance.
- [ ] Toàn bộ server đã được dừng sau khi hoàn thành.
