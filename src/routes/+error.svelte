<script lang="ts">
  import { page } from "$app/stores";
  import Seo from "$lib/components/Seo.svelte";
</script>

<Seo title="Not Found - Huaijiang Zhu" description="Page not found" />

<article class="layout-md text-center py-20">
  <h1 class="text-6xl font-bold text-black dark:text-white mb-4">
    {$page.status}
  </h1>
  <p class="text-xl text-neutral-600 dark:text-neutral-400 mb-8">
    {$page.error?.message || "Page not found"}
  </p>
  <a
    href="/"
    class="inline-block px-6 py-3 bg-neutral-900 dark:bg-white text-white dark:text-black rounded-lg hover:opacity-80 transition-opacity"
  >
    Go back home
  </a>
</article>
