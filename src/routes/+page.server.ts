import type { PageServerLoad } from "./$types";

interface SubstackPost {
  title: string;
  date: string;
  url: string;
  timestamp: number;
  external: boolean;
}

interface PostModule {
  title: string;
  date: string;
  slug?: string;
}

function formatDateET(date: Date): string {
  return date.toLocaleDateString("en-US", {
    timeZone: "America/New_York",
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

function slugFromUrl(url: string): string {
  const match = url.match(/\/p\/([^/?#]+)/);
  return match ? match[1] : "";
}

export const load: PageServerLoad = async ({ fetch }) => {
  // Load local posts from markdown files
  const postModules = import.meta.glob<PostModule>("../posts/*.md", {
    eager: true,
  });

  const localPosts = Object.entries(postModules).map(([path, post]) => {
    const filename = path.split("/").pop()?.replace(".md", "") ?? "";
    const slug = post.slug || filename;
    const date = new Date(post.date);
    return {
      slug,
      title: post.title,
      url: `/notes/${slug}`,
      date: formatDateET(date),
      timestamp: date.getTime(),
      external: false,
    };
  });

  // Load Substack newsletter posts
  let substackPosts: SubstackPost[] = [];
  try {
    const response = await fetch("https://huaijiang.substack.com/feed");
    const xml = await response.text();

    const itemRegex = /<item>([\s\S]*?)<\/item>/g;
    let match;

    while ((match = itemRegex.exec(xml)) !== null) {
      const itemContent = match[1];

      const titleMatch = itemContent.match(
        /<title><!\[CDATA\[(.*?)\]\]><\/title>/,
      );
      const linkMatch = itemContent.match(/<link>(.*?)<\/link>/);
      const pubDateMatch = itemContent.match(/<pubDate>(.*?)<\/pubDate>/);

      if (titleMatch && linkMatch && pubDateMatch) {
        const pubDate = new Date(pubDateMatch[1]);
        substackPosts.push({
          title: titleMatch[1],
          url: linkMatch[1],
          date: formatDateET(pubDate),
          timestamp: pubDate.getTime(),
          external: true,
        });
      }
    }
  } catch (error) {
    console.error("Failed to fetch Substack feed:", error);
  }

  // Merge: Substack posts take priority, local posts fill in gaps (dedup by slug)
  const seenSlugs = new Set(substackPosts.map((p) => slugFromUrl(p.url)));
  const mergedPosts = [...substackPosts];

  for (const post of localPosts) {
    if (!seenSlugs.has(post.slug)) {
      mergedPosts.push(post);
    }
  }

  mergedPosts.sort((a, b) => b.timestamp - a.timestamp);

  return { substackPosts: mergedPosts.slice(0, 5) };
};
