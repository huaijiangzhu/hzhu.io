import type { PageLoad } from "./$types";
import type { EntryGenerator } from "./$types";

interface PostModule {
  title: string;
  date: string;
  description: string;
  slug?: string;
  content: string;
}

const postModules = import.meta.glob<PostModule>("/src/posts/*.md", {
  eager: true,
});

export const entries: EntryGenerator = () => {
  return Object.entries(postModules).map(([path, post]) => {
    const filename = path.split("/").pop()?.replace(".md", "") ?? "";
    return { slug: post.slug || filename };
  });
};

export const load: PageLoad = async ({ params }) => {
  // Find the post by slug
  for (const [path, post] of Object.entries(postModules)) {
    const filename = path.split("/").pop()?.replace(".md", "") ?? "";
    const slug = post.slug || filename;
    if (slug === params.slug) {
      return {
        title: post.title,
        date: new Date(post.date),
        description: post.description,
        content: post.content,
      };
    }
  }

  throw new Error(`Post not found: ${params.slug}`);
};
