import { marked } from 'marked'
import { getImageUrl } from './request'

/**
 * 将 Markdown 内容转换为 HTML
 * 并将图片路径转换为完整的后端 URL
 */
export function parseMarkdown(markdown: string): string {
  if (!markdown) return ''

  // 配置 marked
  marked.setOptions({
    breaks: true, // 支持换行
    gfm: true // 支持 GitHub Flavored Markdown
  })

  // 转换 Markdown 为 HTML
  let html = marked.parse(markdown) as string

  // 处理图片路径：将相对路径转换为完整 URL，并添加样式
  // 匹配 <img src="/uploads/..." /> 或 <img src="uploads/..." />
  html = html.replace(
    /<img([^>]*?)src=["']([^"']+)["']([^>]*?)>/gi,
    (match, before, src, after) => {
      // 转换图片路径为完整 URL
      const fullUrl = getImageUrl(src)
      // 添加样式：宽度100%，高度自适应
      return `<img${before}src="${fullUrl}" style="width: 100%; height: auto; display: block; margin: 20px 0;"${after}>`
    }
  )

  return html
}

/**
 * 从 Markdown 内容中提取第一张图片的 URL
 */
export function extractFirstImage(markdown: string): string {
  if (!markdown) return ''

  // 匹配 Markdown 图片语法: ![alt](url)
  const markdownImageRegex = /!\[.*?\]\(([^)]+)\)/
  const match = markdown.match(markdownImageRegex)

  if (match && match[1]) {
    return match[1]
  }

  return ''
}
