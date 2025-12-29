# Markdown 处理工具
import re
from typing import Optional


def extract_first_image(markdown_content: str) -> Optional[str]:
    """
    从 Markdown 内容中提取第一张图片的 URL
    
    支持的格式:
    - ![alt](url)
    - <img src="url">
    
    Args:
        markdown_content: Markdown 格式的内容
        
    Returns:
        第一张图片的 URL，如果没有图片则返回 None
    """
    if not markdown_content:
        return None
    
    # 匹配 Markdown 图片语法: ![alt](url)
    md_pattern = r'!\[.*?\]\((.*?)\)'
    md_match = re.search(md_pattern, markdown_content)
    if md_match:
        return md_match.group(1)
    
    # 匹配 HTML img 标签: <img src="url">
    html_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
    html_match = re.search(html_pattern, markdown_content)
    if html_match:
        return html_match.group(1)
    
    return None


def markdown_to_html(markdown_content: str) -> str:
    """
    将 Markdown 转换为 HTML
    
    简单实现，支持基本语法:
    - 标题 (# ## ###)
    - 粗体 (**text**)
    - 斜体 (*text*)
    - 图片 (![alt](url))
    - 链接 ([text](url))
    - 段落
    
    Args:
        markdown_content: Markdown 格式的内容
        
    Returns:
        HTML 格式的内容
    """
    if not markdown_content:
        return ""
    
    html = markdown_content
    
    # 标题
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # 粗体
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'__(.*?)__', r'<strong>\1</strong>', html)
    
    # 斜体
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    html = re.sub(r'_(.*?)_', r'<em>\1</em>', html)
    
    # 图片
    html = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1" />', html)
    
    # 链接
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)
    
    # 段落（简单处理：空行分隔）
    paragraphs = html.split('\n\n')
    html_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        if p and not p.startswith('<'):
            p = f'<p>{p}</p>'
        html_paragraphs.append(p)
    
    html = '\n'.join(html_paragraphs)
    
    return html
