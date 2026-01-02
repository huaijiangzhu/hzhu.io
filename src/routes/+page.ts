import type { PageLoad } from "./$types";

interface PostModule {
  title: string;
  date: string;
  description: string;
  slug?: string;
  content: string;
}

export const load: PageLoad = async () => {
  const postModules = import.meta.glob<PostModule>("../posts/*.md", {
    eager: true,
  });

  const posts = Object.entries(postModules)
    .map(([path, post]) => {
      const filename = path.split("/").pop()?.replace(".md", "") ?? "";
      return {
        slug: post.slug || filename,
        title: post.title,
        date: new Date(post.date),
        description: post.description,
      };
    })
    .sort((a, b) => b.date.getTime() - a.date.getTime())
    .slice(0, 3);

  return { posts };
};
