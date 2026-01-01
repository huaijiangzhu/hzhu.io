<script lang="ts">
  import { Github, Twitter, Linkedin, Mail } from "lucide-svelte";

  const links = [
    {
      label: "github",
      href: "https://github.com/huaijiangzhu",
      handle: "@huaijiangzhu",
    },
    {
      label: "twitter",
      href: "https://twitter.com/huaijiangzhu",
      handle: "@huaijiangzhu",
    },
    {
      label: "linkedin",
      href: "https://linkedin.com/in/huaijiangzhu",
      handle: "huaijiangzhu",
    },
  ];
</script>

<footer class="layout-md mt-20 text-lg flex flex-col">
  {#each links as link}
    <div class="row">
      <span>{link.label}</span>
      <hr />
      <a class="link" href={link.href} target="_blank" rel="noopener noreferrer"
        >{link.handle}</a
      >
    </div>
  {/each}
  <p class="mt-8 text-sm text-neutral-500 dark:text-neutral-400">
    based on <a href="https://github.com/ekzhang/ekzhang.github.io" class="link" target="_blank" rel="noopener noreferrer">ekzhang.github.io</a>
  </p>
</footer>

<style lang="postcss">
  .row {
    @apply flex items-center space-x-4;
  }

  .row span {
    @apply text-neutral-500 dark:text-neutral-400 min-w-[70px];
  }

  .row hr {
    @apply w-full mt-0.5 border-neutral-300 dark:border-neutral-700 border-dotted;
  }
</style>
