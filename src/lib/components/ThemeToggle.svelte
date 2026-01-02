<script lang="ts">
  import { browser } from "$app/environment";
  import { Sun, Moon } from "lucide-svelte";

  let isDark = false;

  if (browser) {
    isDark = document.documentElement.classList.contains("dark");
  }

  function toggle() {
    isDark = !isDark;
    if (isDark) {
      document.documentElement.classList.add("dark");
      localStorage.theme = "dark";
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.theme = "light";
    }
  }
</script>

<button
  on:click={toggle}
  class="p-2 rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-colors"
  aria-label="Toggle dark mode"
>
  {#if isDark}
    <Sun class="w-6 h-6" />
  {:else}
    <Moon class="w-6 h-6" />
  {/if}
</button>
