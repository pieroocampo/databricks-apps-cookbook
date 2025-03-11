import { themes as prismThemes } from "prism-react-renderer";
import type { Config } from "@docusaurus/types";
import type * as Preset from "@docusaurus/preset-classic";

const config: Config = {
  title: "Databricks Apps Cookbook",
  tagline:
    "Ready-to-use code snippets for building data and AI applications using Databricks Apps",
  favicon: "img/favicon.ico",

  url: "https://apps-cookbook.dev",
  baseUrl: "/",

  organizationName: "pbv0",
  projectName: "databricks-apps-cookbook",

  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",

  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },

  presets: [
    [
      "classic",
      {
        docs: {
          sidebarPath: "./sidebars.ts",
          editUrl: "https://github.com/pbv0/databricks-apps-cookbook/docs/",
        },
        blog: false,
        theme: {
          customCss: "./src/css/custom.css",
        },
      } satisfies Preset.Options,
    ],
  ],

  plugins: [
    require.resolve("docusaurus-lunr-search"),
    function tailwindPlugin(context, options) {
      return {
        name: "tailwind-plugin",
        configurePostCss(postcssOptions) {
          postcssOptions.plugins = [require("@tailwindcss/postcss")];
          return postcssOptions;
        },
      };
    },
  ],

  themeConfig: {
    image: "img/og-image.png",
    metadata: [
      {
        name: "keywords",
        content: "databricks, databricks apps, streamlit, dash",
      },
    ],
    navbar: {
      title: "Databricks Apps Cookbook",
      items: [
        {
          to: "docs/intro",
          label: "Introduction",
          position: "left",
          activeBasePath: "docs/intro",
        },
        {
          to: "docs/category/streamlit",
          label: "Streamlit",
          position: "left",
          activeBasePath: "docs/category/streamlit",
        },
        {
          to: "docs/category/dash",
          label: "Dash",
          position: "left",
          activeBasePath: "docs/category/dash",
        },
        {
          href: "https://github.com/pbv0/databricks-apps-cookbook/",
          label: "GitHub",
          position: "right",
        },
      ],
    },
    footer: {
      copyright: `Copyright © ${new Date().getFullYear()} Databricks Apps Cookbook. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.vsLight,
      darkTheme: prismThemes.vsDark,
      additionalLanguages: ["bash"],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
