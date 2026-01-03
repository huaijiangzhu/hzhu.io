import type { PageServerLoad } from "./$types";

interface SubstackPost {
  title: string;
  date: string;
  url: string;
  timestamp: number;
}

function formatDateET(date: Date): string {
  return date.toLocaleDateString("en-US", {
    timeZone: "America/New_York",
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

export const load: PageServerLoad = async ({ fetch }) => {
  // Load Substack newsletter posts
  let substackPosts: SubstackPost[] = [];
  try {
    const response = await fetch("https://huaijiang.substack.com/feed");
    const xml = await response.text();

    const itemRegex = /<item>([\s\S]*?)<\/item>/g;
    let match;

    while ((match = itemRegex.exec(xml)) !== null) {
      const itemContent = match[1];

      const titleMatch = itemContent.match(/<title><!\[CDATA\[(.*?)\]\]><\/title>/);
      const linkMatch = itemContent.match(/<link>(.*?)<\/link>/);
      const pubDateMatch = itemContent.match(/<pubDate>(.*?)<\/pubDate>/);

      if (titleMatch && linkMatch && pubDateMatch) {
        const pubDate = new Date(pubDateMatch[1]);
        substackPosts.push({
          title: titleMatch[1],
          url: linkMatch[1],
          date: formatDateET(pubDate),
          timestamp: pubDate.getTime(),
        });
      }
    }

    substackPosts.sort((a, b) => b.timestamp - a.timestamp);
    substackPosts = substackPosts.slice(0, 5);
  } catch (error) {
    console.error("Failed to fetch Substack feed:", error);
  }

  return { substackPosts };
};
