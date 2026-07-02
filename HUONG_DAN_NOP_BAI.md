# Hướng dẫn nộp Lab 26

## Thành phần cần hoàn thành

Theo yêu cầu trong notebook:

1. Chạy đủ năm prompt ADK Web từ W1 đến W5.
2. Điền cell `adk_web_results` và bảo đảm kết quả cuối là `5/5` nếu cả năm prompt đã chạy thành công.
3. Hoàn thành checklist Capstone.
4. Kiểm tra có Trace ID trong session state.
5. Kiểm tra Trace có các agent/tool tương ứng.
6. Kiểm tra audit tại `logs/governance_audit.jsonl`.
7. Nộp notebook kèm screenshot ADK Web, ít nhất W1 và W2.

Notebook không yêu cầu một file report riêng. Nếu giảng viên không có yêu cầu bổ sung ngoài notebook, chỉ cần notebook đã chạy và ảnh minh chứng.

## Screenshot bắt buộc

### Ảnh 1 — W1: A2A Search

Hiển thị trong cùng ảnh:

- prompt W1;
- câu trả lời cuối của `search_agent`;
- tab Trace có `transfer_to_agent` hoặc `search_agent`;
- URL/trang ADK Web nếu khung hình cho phép.

Tên file gợi ý:

```text
W1_A2A_search_agent.png
```

### Ảnh 2 — W2: MCP multi-tool

Hiển thị trong cùng ảnh:

- prompt W2;
- báo cáo tóm tắt cuối;
- tab Trace có `search_documents` và `sql_query`.

Tên file gợi ý:

```text
W2_MCP_search_sql.png
```

## Screenshot khuyến nghị thêm

Không bắt buộc theo câu chữ trong notebook, nhưng nên chụp để bài nộp rõ ràng:

- `W3_synthesis_agent.png`: Trace có `synthesis_agent` và báo cáo executive.
- `W4_suggest_routing.png`: kết quả chọn `database_agent` cho SQL/metrics.
- `W5_governance_deny.png`: yêu cầu `DROP TABLE` bị từ chối.
- `A2A_servers_OK.png`: ba specialist trên cổng 8001–8003 đều OK.
- `governance_audit.png`: năm dòng cuối audit log.

## Lấy audit log

Trong terminal:

```bash
cd /home/elio12/projects/Day26-2A202601010-TranQuangHuy
tail -5 logs/governance_audit.jsonl
```

Có thể chụp terminal này làm bằng chứng observability/governance.

## Checklist trước khi nộp

- [ ] Notebook mở và chạy bằng kernel `pii-env`.
- [ ] Cell kiểm tra ba A2A specialist đều có dấu `✓` hoặc `ĐẠT`.
- [ ] W1–W5 đều ghi `ĐẠT` trong cell kết quả.
- [ ] Tổng kết cell hiển thị `Tổng: 5/5 prompt đạt yêu cầu`.
- [ ] Có ảnh W1 và W2.
- [ ] Trace ID xuất hiện trong session state.
- [ ] Audit log có dữ liệu.
- [ ] Lưu notebook sau khi chạy cell: `Ctrl+S`.
- [ ] Không nộp file `.env` và không để lộ `OPENAI_API_KEY` trong screenshot.

## Bộ file nên nộp

Tối thiểu:

```text
day26_mcp_a2a_lab.ipynb
W1_A2A_search_agent.png
W2_MCP_search_sql.png
```

Nếu hệ thống nộp bài cho phép nộp cả project, nén project nhưng loại bỏ `.env`, log không cần thiết và API key.
