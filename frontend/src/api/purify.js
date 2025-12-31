import DOMPurify from "dompurify";

// Sanitize 
export function sanitizeHTML(dirty) {
  return DOMPurify.sanitize(dirty, {
    ALLOWED_ATTR: ["class", "style", "href", "src", "alt", "title"],

    ALLOWED_TAGS: [
      "pre",
      "div",
      "span",
      "p",
      "b",
      "i",
      "u",
      "strong",
      "em",
      "ul",
      "ol",
      "li",
      "br",
      "img",
      "a",
      "h1",
      "h2",
      "h3",

      // table tags
      "table",
      "thead",
      "tbody",
      "tfoot",
      "tr",
      "th",
      "td",
      "caption",
      "col",
      "colgroup"
    ],
    FORBID_TAGS: ["script", "iframe", "object", "embed"],
    FORBID_ATTR: ["onerror", "onclick", "onload"]
  });
}
