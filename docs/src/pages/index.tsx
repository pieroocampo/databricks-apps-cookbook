import type { ReactNode } from "react";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Layout from "@theme/Layout";
import Heading from "@theme/Heading";
import HeaderAnimation from "../components/HeaderAnimation";
import { useColorMode } from "@docusaurus/theme-common";

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  const { isDarkTheme } = useColorMode();

  return (
    <div className="relative flex h-full w-full flex-1 items-center justify-center overflow-hidden">
      <HeaderAnimation isDarkMode={isDarkTheme} />
      <div className="absolute z-10 flex w-full flex-col items-center justify-center px-4 text-center text-white sm:px-6">
        <Heading
          as="h1"
          className="text-3xl font-bold text-gray-800 sm:text-5xl lg:text-7xl dark:text-white"
        >
          {siteConfig.title}
        </Heading>
        <p className="mt-3 max-w-3xl text-lg leading-relaxed text-gray-800 sm:mt-4 sm:text-xl sm:leading-10 lg:text-3xl dark:text-white">
          {siteConfig.tagline}
        </p>
        <div className="mt-6 flex w-full max-w-md flex-col items-center justify-center space-y-3 sm:mt-8 sm:max-w-none sm:flex-row sm:space-y-0 sm:space-x-4">
          <Link to="/docs/category/streamlit" className="w-full sm:w-auto">
            <button className="w-full border-2 border-lava-600 bg-lava-600 px-6 py-2.5 align-middle text-base font-semibold text-white transition-colors hover:cursor-pointer hover:border-lava-700 hover:bg-lava-700 hover:underline sm:w-auto sm:px-8 sm:text-lg">
              Streamlit
            </button>
          </Link>
          <Link to="/docs/category/dash" className="w-full sm:w-auto">
            <button className="w-full border-2 border-lava-600 bg-lava-600 px-6 py-2.5 align-middle text-base font-semibold text-white transition-colors hover:cursor-pointer hover:border-lava-700 hover:bg-lava-700 hover:underline sm:w-auto sm:px-8 sm:text-lg">
              Dash
            </button>
          </Link>
          <Link to="/docs/intro" className="w-full sm:w-auto">
            <button className="w-full border-2 border-gray-800 bg-transparent px-6 py-2.5 align-middle text-base font-semibold text-gray-800 transition-colors hover:cursor-pointer hover:underline sm:w-auto sm:px-8 sm:text-lg dark:border-white dark:text-white">
              Learn more
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
}

export default function Home(): ReactNode {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout description={`${siteConfig.tagline}`}>
      <HomepageHeader />
    </Layout>
  );
}
