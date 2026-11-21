# Notice: material adapted from Higgsfield skills

Eight of the skills are adapted from **higgsfield-ai/skills** (https://github.com/higgsfield-ai/skills), version 0.14.0:

| OyJI skill | Adapted from |
|---|---|
| `oyji-product-photoshoot` | `higgsfield-product-photoshoot` |
| `oyji-marketplace-cards` | `higgsfield-marketplace-cards` |
| `oyji-faceless-video` | `higgsfield-faceless-video` |
| `oyji-brandkit` | `higgsfield-brandkit` |
| `oyji-face-id` | `higgsfield-soul-id` |
| `oyji-thumbnail` | `higgsfield-youtube-thumbnail` |
| `oyji-websites` | `higgsfield-websites` |
| `oyji-generate` | `higgsfield-generate` |

`oyji-creature`, `oyji-location` and `oyji-video-director` are our own text.

What was taken: the structure of each workflow (the modes and scopes, the interview flow, the asset lists, the Brand Lock and
approval sequence, the production and QC gates for narrated video, the one-time setup and reuse pattern, the model-picking and
delivery rules). What was changed: all tool calls (the Higgsfield CLI replaced by the OyJI MCP and local ffmpeg / Pillow), the models,
the prompt templates (Higgsfield keeps its own on a private server, these were written for OyJI), the market (Kazakhstan: Kaspi, Satu,
Kazakh and Russian text) and the helper scripts (written new).

The original work is licensed as follows, and this notice must stay with any copy of the adapted skills:

MIT License

Copyright (c) 2026 Higgsfield AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
