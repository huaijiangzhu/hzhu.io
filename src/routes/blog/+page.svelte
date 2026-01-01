<script lang="ts">
  import Seo from "$lib/components/Seo.svelte";
  import { formatFullDate } from "$lib/utils";
  import type { PageData } from "./$types";

  export let data: PageData;
</script>

<Seo
  title="Blog - Huaijiang Zhu"
  description="Blog posts about robotics, machine learning, and other topics."
/>

<article class="layout-md">
  <h2 class="heading2">Blog</h2>

  <div class="space-y-8">
    {#each data.posts as post}
      <a href="/blog/{post.slug}" class="block group">
        <article>
          <h3
            class="font-medium text-black dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors mb-1"
          >
            {post.title}
          </h3>
          <p class="text-sm text-neutral-500 dark:text-neutral-400 mb-2">
            {formatFullDate(post.date)}
          </p>
          <p class="text-neutral-600 dark:text-neutral-300">
            {post.description}
          </p>
        </article>
      </a>
    {/each}
  </div>

  {#if data.posts.length === 0}
    <p class="text-neutral-500 dark:text-neutral-400">No posts yet.</p>
  {/if}
</article>
