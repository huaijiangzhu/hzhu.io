<script lang="ts">
  import Seo from "$lib/components/Seo.svelte";
  import { formatFullDate } from "$lib/utils";
  import type { PageData } from "./$types";

  export let data: PageData;
</script>

<Seo
  title="诸怀疆 | Huaijiang Zhu"
  description="Founding engineer at Alquist working on multimodal reasoning for embodied agents. Ph.D. from NYU in robotics."
/>

<article class="layout-md">
  <section>
    <h1 class="text-2xl font-bold text-black dark:text-white mb-6">诸怀疆 | Huaijiang Zhu</h1>
    <div>
      <img
        src="/images/profile.jpg"
        alt="Huaijiang Zhu"
        class="float-right ml-6 mb-4 w-44 h-44 rounded-full object-cover shadow-lg"
      />
      <p>
        I am a founding engineer at <a
          href="https://www.alquistrobotics.com/"
          class="link"
          target="_blank"
          rel="noopener noreferrer">Alquist</a
        > working on multimodal reasoning for embodied agents. I received my Ph.D.
        from New York University, where I was advised by Prof.
        <a
          href="https://engineering.nyu.edu/faculty/ludovic-righetti"
          class="link"
          target="_blank"
          rel="noopener noreferrer">Ludovic Righetti</a
        >
        at the
        <a
          href="http://www.machinesinmotion.org/"
          class="link"
          target="_blank"
          rel="noopener noreferrer">Machines in Motion Laboratory</a
        >. During my Ph.D., I interned at the Boston Dynamics
        <a
          href="https://rai-inst.com/"
          class="link"
          target="_blank"
          rel="noopener noreferrer">RAI Institute</a
        >, working with Dr.
        <a
          href="https://pangtao.xyz/"
          class="link"
          target="_blank"
          rel="noopener noreferrer">Tao Pang</a
        > on contact-rich dexterous manipulation. Prior to NYU, I received my bachelor's
        and master's degree in Electrical Engineering from the
        <a
          href="https://www.tum.de/"
          class="link"
          target="_blank"
          rel="noopener noreferrer">Technical University of Munich</a
        >.
      </p>
    </div>
  </section>

  {#if data.posts.length > 0}
    <section class="mt-12">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-bold text-black dark:text-white">Recent Posts</h2>
        <a href="/blog" class="text-sm link">View all</a>
      </div>

      <div class="space-y-6">
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
    </section>
  {/if}

</article>
