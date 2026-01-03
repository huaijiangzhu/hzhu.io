<script lang="ts">
  import { page } from "$app/stores";
  import ThemeToggle from "./ThemeToggle.svelte";

  const links = [
    { name: "publications", href: "/publications" },
    { name: "notes", href: "/notes" },
    { name: "newsletter", href: "https://huaijiang.substack.com", external: true },
  ];
</script>

<header
  class="layout-md mb-8 flex justify-between items-center"
  data-sveltekit-noscroll
  data-sveltekit-preload-code="eager"
>
  <nav>
    <a
      href="/"
      class="hover:text-black dark:hover:text-white transition-colors"
      class:text-black={$page.url.pathname === "/"}
      class:dark:text-white={$page.url.pathname === "/"}
    >
      about
    </a>
    {#each links as link (link)}
      <a
        href={link.href}
        class="hover:text-black dark:hover:text-white transition-colors"
        class:text-black={!link.external && ($page.url.pathname === link.href ||
          $page.url.pathname.startsWith(link.href + "/"))}
        class:dark:text-white={!link.external && ($page.url.pathname === link.href ||
          $page.url.pathname.startsWith(link.href + "/"))}
        target={link.external ? "_blank" : undefined}
        rel={link.external ? "noopener noreferrer" : undefined}
      >
        {link.name}
      </a>
    {/each}
  </nav>
  <ThemeToggle />
</header>

<style lang="postcss">
  nav {
    @apply flex items-center text-neutral-500 dark:text-neutral-400 justify-start space-x-6 text-lg;
  }

  @media (max-width: 420px) {
    nav {
      @apply flex-wrap gap-4 space-x-0;
    }
  }
</style>
