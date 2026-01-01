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

  function renderMath(content: string): string {
    // Render display math ($$...$$)
    content = content.replace(/\$\$([\s\S]+?)\$\$/g, (_, math) => {
      try {
        return katex.renderToString(math.trim(), {
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
        return katex.renderToString(math.trim(), {
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

<style lang="postcss">
  .md-output :global(p) {
    @apply mb-4;
  }

  .md-output :global(strong) {
    @apply font-semibold text-black dark:text-white;
  }

  .md-output :global(em) {
    @apply italic;
  }

  .md-output :global(code) {
    @apply text-[95%] bg-neutral-100 dark:bg-neutral-800 px-1.5 py-0.5 rounded;
  }

  .md-output :global(pre) {
    @apply bg-neutral-100 dark:bg-neutral-800 p-4 rounded-lg overflow-x-auto mb-4;
  }

  .md-output :global(pre code) {
    @apply bg-transparent p-0;
  }

  .md-output :global(ul) {
    @apply list-disc list-inside mb-4;
  }

  .md-output :global(ol) {
    @apply list-decimal list-inside mb-4;
  }

  .md-output :global(li) {
    @apply mb-1;
  }

  .md-output :global(h1) {
    @apply text-2xl font-bold text-black dark:text-white mb-4 mt-8;
  }

  .md-output :global(h2) {
    @apply text-xl font-semibold text-black dark:text-white mb-3 mt-6;
  }

  .md-output :global(h3) {
    @apply text-lg font-medium text-black dark:text-white mb-2 mt-4;
  }

  .md-output :global(blockquote) {
    @apply border-l-4 border-neutral-300 dark:border-neutral-600 pl-4 italic text-neutral-600 dark:text-neutral-400 mb-4;
  }

  .md-output :global(.katex-display) {
    @apply overflow-x-auto py-2;
  }
</style>
