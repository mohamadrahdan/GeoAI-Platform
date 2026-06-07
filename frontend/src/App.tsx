import { ErrorBoundary } from "@/components/common/ErrorBoundary";
import { HomePage } from "@/pages/HomePage";

export default function App() {
  return (
    <ErrorBoundary>
      <HomePage />
    </ErrorBoundary>
  );
}