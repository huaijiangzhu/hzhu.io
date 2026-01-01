<script lang="ts">
  import { ExternalLink, Video, Code, FileText, Globe } from "lucide-svelte";

  export let publication: {
    id: string;
    title: string;
    authors: Array<{ name: string; self?: boolean }>;
    venue: string;
    year: number;
    teaser?: string;
    arxiv?: string;
    pdf?: string;
    code?: string;
    video?: string;
    website?: string;
    selected?: boolean;
    award?: string;
  };

  function formatAuthors(
    authors: Array<{ name: string; self?: boolean }>
  ): string {
    return authors
      .map((a) => (a.self ? `<strong>${a.name}</strong>` : a.name))
      .join(", ");
  }
</script>

<article class="flex flex-col sm:flex-row gap-4 mb-8">
  {#if publication.teaser}
    <div class="sm:w-32 flex-shrink-0">
      <img
        src="/images/teasers/{publication.teaser}"
        alt={publication.title}
        class="w-full h-auto rounded-lg border border-neutral-200 dark:border-neutral-700"
      />
    </div>
  {/if}
  <div class="flex-1">
    <h3 class="font-medium text-black dark:text-white mb-1">
      {publication.title}
    </h3>
    <p class="text-sm text-neutral-600 dark:text-neutral-400 mb-1">
      {@html formatAuthors(publication.authors)}
    </p>
    <p class="text-sm text-neutral-500 dark:text-neutral-500 mb-2">
      {publication.venue}, {publication.year}
    </p>
    {#if publication.award}
      <p class="text-sm text-orange-600 dark:text-orange-400 font-medium mb-2">
        {publication.award}
      </p>
    {/if}
    <div class="flex flex-wrap gap-2">
      {#if publication.arxiv}
        <a
          href="https://arxiv.org/abs/{publication.arxiv}"
          target="_blank"
          rel="noopener noreferrer"
          class="inline-flex items-center gap-1 text-xs px-2 py-1 bg-neutral-100 dark:bg-neutral-800 rounded hover:bg-neutral-200 dark:hover:bg-neutral-700 transition-colors"
        >
          <FileText class="w-3 h-3" />
          arXiv
        </a>
      {/if}
      {#if publication.pdf}
        <a
          href="/pdf/{publication.pdf}"
          target="_blank"
          rel="noopener noreferrer"
          class="inline-flex items-center gap-1 text-xs px-2 py-1 bg-neutral-100 dark:bg-neutral-800 rounded hover:bg-neutral-200 dark:hover:bg-neutral-700 transition-colors"
        >
          <FileText class="w-3 h-3" />
          PDF
        </a>
      {/if}
      {#if publication.code}
        <a
          href={publication.code}
          target="_blank"
          rel="noopener noreferrer"
          class="inline-flex items-center gap-1 text-xs px-2 py-1 bg-neutral-100 dark:bg-neutral-800 rounded hover:bg-neutral-200 dark:hover:bg-neutral-700 transition-colors"
        >
          <Code class="w-3 h-3" />
          Code
        </a>
      {/if}
      {#if publication.video}
        <a
          href={publication.video}
          target="_blank"
          rel="noopener noreferrer"
          class="inline-flex items-center gap-1 text-xs px-2 py-1 bg-neutral-100 dark:bg-neutral-800 rounded hover:bg-neutral-200 dark:hover:bg-neutral-700 transition-colors"
        >
          <Video class="w-3 h-3" />
          Video
        </a>
      {/if}
      {#if publication.website}
        <a
          href={publication.website}
          target="_blank"
          rel="noopener noreferrer"
          class="inline-flex items-center gap-1 text-xs px-2 py-1 bg-neutral-100 dark:bg-neutral-800 rounded hover:bg-neutral-200 dark:hover:bg-neutral-700 transition-colors"
        >
          <Globe class="w-3 h-3" />
          Website
        </a>
      {/if}
    </div>
  </div>
</article>
