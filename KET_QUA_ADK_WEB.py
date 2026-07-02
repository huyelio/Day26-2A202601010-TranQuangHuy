# 📝 KẾT QUẢ ADK WEB — copy toàn bộ nội dung file này vào cell kết quả

adk_web_results = [
    {
        "prompt_id": "W1",
        "agents_involved": ["orchestrator", "search_agent"],
        "tools_or_protocol": "A2A",
        "outcome": "ĐẠT",
        "notes": "Đã transfer sang search_agent và trả về 2 kết quả về MCP/A2A cho truy vấn multi-agent orchestration.",
    },
    {
        "prompt_id": "W2",
        "agents_involved": ["orchestrator"],
        "tools_or_protocol": "MCP (search_documents, sql_query)",
        "outcome": "ĐẠT",
        "notes": "Đã gọi search_documents và sql_query, sau đó tổng hợp tài liệu MCP cùng metrics của 3 agent.",
    },
    {
        "prompt_id": "W3",
        "agents_involved": ["orchestrator", "synthesis_agent"],
        "tools_or_protocol": "A2A → synthesis_agent",
        "outcome": "ĐẠT",
        "notes": "Đã transfer sang synthesis_agent và nhận báo cáo executive tổng hợp findings về MCP và A2A.",
    },
    {
        "prompt_id": "W4",
        "agents_involved": ["orchestrator"],
        "tools_or_protocol": "suggest_routing",
        "outcome": "ĐẠT",
        "notes": "Đã gọi suggest_routing và giải thích database_agent là lựa chọn phù hợp cho truy vấn SQL/metrics.",
    },
    {
        "prompt_id": "W5",
        "agents_involved": ["orchestrator"],
        "tools_or_protocol": "MCP sql_query — governance deny",
        "outcome": "ĐẠT",
        "notes": "Yêu cầu DROP TABLE bị từ chối vì vi phạm chính sách SQL chỉ đọc.",
    },
]

print(f"{'ID':<4} {'Agents':<35} {'Protocol':<28} {'Kết quả':<12} Ghi chú")
print("-" * 100)
for row in adk_web_results:
    agents = ", ".join(row["agents_involved"])
    print(
        f"{row['prompt_id']:<4} {agents:<35} "
        f"{row['tools_or_protocol']:<28} {row['outcome']:<12} {row['notes']}"
    )

passed = sum(1 for result in adk_web_results if result["outcome"] == "ĐẠT")
print(f"\nTổng: {passed}/{len(adk_web_results)} prompt đạt yêu cầu")
print("\n💡 Nộp notebook kèm screenshot ADK Web (ít nhất W1 và W2).")
