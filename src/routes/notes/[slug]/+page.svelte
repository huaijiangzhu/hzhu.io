<script lang="ts">
  import Seo from "$lib/components/Seo.svelte";
  import Markdown from "$lib/components/Markdown.svelte";
  import { formatFullDate } from "$lib/utils";
  import type { PageData } from "./$types";

  export let data: PageData;
</script>

<Seo title="{data.title} - Huaijiang Zhu" description={data.description} />

<article class="layout-md">
  <header class="mb-8">
    <h1 class="text-2xl font-bold text-black dark:text-white mb-2">
      {data.title}
    </h1>
    <p class="text-neutral-500 dark:text-neutral-400">
      {formatFullDate(data.date)}
    </p>
  </header>

  <div class="prose">
    <Markdown source={data.content} />
  </div>

  <div class="mt-12 pt-8 border-t border-neutral-200 dark:border-neutral-700">
    <a
      href="/notes"
      class="text-neutral-500 dark:text-neutral-400 hover:text-black dark:hover:text-white transition-colors"
    >
      &larr; Back to all notes
    </a>
  </div>
</article>
