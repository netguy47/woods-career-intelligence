import shutil

src = r"D:\blogger\jobspy-mcp-server\phase2_execution_log.md"
dst = r"D:\blogger\jobspy-mcp-server\phase2_review_package\phase2_execution_log.md"
shutil.copy2(src, dst)
print("Updated phase2_execution_log.md in review package.")
