import { redirect } from "next/navigation";

export default async function AttentionPage({
  params,
}: {
  params: Promise<{ projectId: string }>;
}) {
  const { projectId } = await params;
  redirect(`/projects/${projectId}/issues`);
}
