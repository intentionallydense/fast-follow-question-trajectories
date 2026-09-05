import type { Metadata } from 'next';
import LegacyTasks from '../tasks/legacy';
export const metadata: Metadata = { title: 'Legacy task reconstructions', description: 'Earlier task reconstructions, preserved separately from the audited trajectory task browser.' };
export default function Page() { return <LegacyTasks />; }
