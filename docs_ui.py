"""Styles for the interactive API reference."""

DOCS_HEAD = """
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body { margin: 0; background: #f4f7f5; }
  .swagger-ui { color: #18382d; }
  .swagger-ui .wrapper { max-width: 1100px; padding-inline: clamp(14px, 4vw, 36px); }
  .swagger-ui .info {
    background: #fff; border: 1px solid #cdded5; border-top: 5px solid #226346;
    border-radius: 16px; padding: clamp(20px, 5vw, 48px); margin: 32px 0 25px;
  }
  .swagger-ui .info .title {
    color: #173d2d; font: 700 clamp(2rem, 6vw, 3.5rem)/1.08 Georgia, serif;
    overflow-wrap: anywhere;
  }
  .swagger-ui .info .description p,
  .swagger-ui .info .description li { font-size: 1rem; line-height: 1.65; }
  .swagger-ui .info .description h3 { color: #173d2d; margin-top: 1.6em; }
  .swagger-ui .info .description a { color: #17603e; text-decoration: underline; }
  .swagger-ui .filter .operation-filter-input,
  .swagger-ui .opblock { border-radius: 8px; }
  .swagger-ui .opblock-tag { color: #173d2d; border-color: #cdded5; }
  .swagger-ui .opblock .opblock-summary-path { overflow-wrap: anywhere; }
  .swagger-ui input:focus-visible, .swagger-ui button:focus-visible,
  .swagger-ui a:focus-visible { outline: 2px solid #226346; outline-offset: 2px; }
  @media (max-width: 600px) {
    .swagger-ui .opblock .opblock-summary { flex-wrap: wrap; row-gap: 5px; }
    .swagger-ui .opblock .opblock-summary-description { padding-block: 4px; }
    .swagger-ui .opblock-tag { flex-wrap: wrap; }
  }
</style>
"""
