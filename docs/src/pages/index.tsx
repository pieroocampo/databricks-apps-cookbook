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
      <div className="absolute z-10 flex w-full flex-col items-center justify-center px-4 text-center text-white md:px-6">
        <Heading
          as="h1"
          className="text-3xl font-bold text-gray-800 md:text-7xl dark:text-white"
        >
          {siteConfig.title}
        </Heading>
        <p className="mt-3 max-w-3xl text-lg leading-relaxed text-gray-800 md:mt-4 md:text-3xl md:leading-10 dark:text-white">
          {siteConfig.tagline}
        </p>
        <div className="mt-6 flex flex-col items-center justify-center space-y-3 md:mt-4 md:flex-row md:space-y-0 md:space-x-8">
          <Link to="/docs/category/streamlit">
            <button className="w-full border-2 border-lava-600 bg-lava-600 px-6 py-2.5 align-middle text-base font-semibold text-white hover:cursor-pointer hover:border-lava-700 hover:bg-lava-700 hover:underline md:w-auto md:px-8 md:text-lg">
              Streamlit
            </button>
          </Link>
          <Link to="/docs/category/dash">
            <button className="w-full border-2 border-lava-600 bg-lava-600 px-6 py-2.5 align-middle text-base font-semibold text-white hover:cursor-pointer hover:border-lava-700 hover:bg-lava-700 hover:underline md:w-auto md:px-8 md:text-lg">
              Dash
            </button>
          </Link>
          <Link to="/docs/intro">
            <button className="w-full border-2 border-gray-800 bg-transparent px-6 py-2.5 align-middle text-base font-semibold text-gray-800 hover:cursor-pointer hover:underline md:w-auto md:px-8 md:text-lg dark:border-white dark:text-white">
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
