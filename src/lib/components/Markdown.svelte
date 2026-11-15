<script lang="ts">
  import { marked } from "marked";
  import katex from "katex";

  export let source: string;

  marked.use({
    renderer: {
      link(href: string, title: string | null, text: string) {
        let out = `<a rel="external" href="${encodeURI(href)}" class="link"`;
        if (title) {
          out += ' title="' + title + '"';
        }
        out += ">" + text + "</a>";
        return out;
      },
    },
  });

  // KaTeX echoes the TeX source verbatim into its MathML <annotation>, newlines
  // included. marked then parses that output, so a lone `-` or `=` line inside
  // display math reads as a setext heading. Collapse newlines first; they are
  // insignificant whitespace in LaTeX anyway.
  function flatten(math: string): string {
    return math.trim().replace(/\s*\n\s*/g, " ");
  }

  function renderMath(content: string): string {
    // Render display math ($$...$$)
    content = content.replace(/\$\$([\s\S]+?)\$\$/g, (_, math) => {
      try {
        return katex.renderToString(flatten(math), {
          displayMode: true,
          throwOnError: false,
        });
      } catch {
        return `<pre class="text-red-500">${math}</pre>`;
      }
    });

    // Render inline math ($...$) but not escaped \$
    content = content.replace(/(?<!\\)\$([^\$\n]+?)\$/g, (_, math) => {
      try {
        return katex.renderToString(flatten(math), {
          displayMode: false,
          throwOnError: false,
        });
      } catch {
        return `<code class="text-red-500">${math}</code>`;
      }
    });

    return content;
  }

  $: processedSource = renderMath(source);
  $: html = marked.parse(processedSource, {
    smartLists: true,
    smartypants: true,
  });
</script>

<div class="md-output">
  {@html html}
</div>
