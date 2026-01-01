<script lang="ts">
  import Seo from "$lib/components/Seo.svelte";
  import Publication from "$lib/components/Publication.svelte";
  import publications from "$lib/../../src/data/publications.yaml";

  // Group publications by year
  const pubsByYear = publications.publications.reduce(
    (acc: Record<number, typeof publications.publications>, pub) => {
      if (!acc[pub.year]) {
        acc[pub.year] = [];
      }
      acc[pub.year].push(pub);
      return acc;
    },
    {}
  );

  const years = Object.keys(pubsByYear)
    .map(Number)
    .sort((a, b) => b - a);
</script>

<Seo
  title="Publications - Huaijiang Zhu"
  description="Research publications in robotics, manipulation, and machine learning."
/>

<article class="layout-md">
  <h2 class="heading2">Publications</h2>
  {#each years as year}
    <div class="mb-8">
      <h3
        class="text-lg font-medium text-neutral-500 dark:text-neutral-400 mb-4"
      >
        {year}
      </h3>
      {#each pubsByYear[year] as pub}
        <Publication publication={pub} />
      {/each}
    </div>
  {/each}
</article>
