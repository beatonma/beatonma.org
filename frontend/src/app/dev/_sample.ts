import { ResponseOf } from "@/api";
import { PostPreview } from "@/components/data/types";
import { MediaFile } from "@/components/media/common";

export const LoremIpsum =
  "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque mattis, orci vel congue vehicula, velit metus cursus nisl, sed condimentum elit libero id diam. Cras pharetra quam vel nisl gravida blandit. Aliquam lorem tellus, mattis at mi dictum, interdum dictum dolor. Ut tempus mauris ut vulputate efficitur. Sed est ligula, aliquam nec porta non, dictum id neque. Donec ornare, nunc ac hendrerit pretium, elit magna sagittis dolor, vel aliquam ipsum lorem ac lorem. Quisque dignissim, dui nec facilisis euismod, lectus leo posuere ligula, sed tempus eros ante ut mi.";

export const SampleMedia: MediaFile[] = [
  {
    url: "/media/related/2025/45f545.jpg",
    thumbnail_url: "/media/related/2025/45f545-thumb.webp",
    type: "image",
    name: "related/2022/45f545.jpg",
    description: "",
    fit: null,
  },
  {
    url: "/media/related/2025/ab909e.jpg",
    thumbnail_url: "/media/related/2025/ab909e-thumb.webp",
    type: "image",
    name: "related/2022/ab909e.jpg",
    description: "",
    fit: null,
  },
  {
    url: "/media/related/2025/3466a3.jpg",
    thumbnail_url: "/media/related/2025/3466a3-thumb.webp",
    type: "image",
    name: "related/2022/3466a3.jpg",
    description: "",
    fit: null,
  },
];

export const SamplePosts: PostPreview[] = [
  {
    post_type: "post",
    title: "Tailwind Prose",
    url: "/posts/202504028a1/",
    is_published: true,
    published_at: "2025-04-02T17:21:01.768Z",
    theme: null,
    hero_embedded_url: null,
    hero_image: null,
    content_html: "Typography check",
    content_script: "",
    files: [],
    is_preview: true,
  },
  {
    post_type: "post",
    title: null,
    url: "/posts/20250301712/",
    is_published: true,
    published_at: "2025-03-01T16:42:09Z",
    theme: {
      muted: "#0E70B8",
      vibrant: "#FDF472",
    },
    hero_embedded_url: null,
    hero_image: null,
    content_html:
      "<p>Hosting for this site is now provided by a European company instead of Amazon.</p>\n\n<p>It&#8217;s an extremely minor thing, but it is a thing nonetheless. 🇺🇦🇪🇺🇬🇧</p>\n",
    content_script: "",
    files: [],
    is_preview: false,
  },
  {
    post_type: "post",
    title: null,
    url: "/posts/2024122259f/",
    is_published: true,
    published_at: "2024-12-22T14:55:33Z",
    theme: null,
    hero_embedded_url: null,
    hero_image: null,
    content_html:
      '<p>A year of incrementally learning Polyphia tunes: <a href="https://www.youtube.com/watch?v=Z5WudJ53zGs" >youtube</a></p>\n',
    content_script: null,
    files: [
      {
        url: "/media/related/2025/68490e.jpg",
        thumbnail_url: "/media/related/2025/68490e-thumb.webp",
        type: "image",
        name: "Capture.JPG",
        description: "",
        fit: null,
      },
    ],
    is_preview: false,
  },
  {
    post_type: "post",
    title: null,
    url: "/posts/20241106d9e/",
    is_published: true,
    published_at: "2024-11-06T07:36:05Z",
    theme: null,
    hero_embedded_url: null,
    hero_image: null,
    content_html: "<p>🤢</p>\n",
    content_script: null,
    files: [],
    is_preview: false,
  },
  {
    post_type: "post",
    title: null,
    url: "/posts/2024103072e/",
    is_published: true,
    published_at: "2024-10-30T22:17:36Z",
    theme: null,
    hero_embedded_url: null,
    hero_image: null,
    content_html: "<p>Jigsaw pumpkin 🎃</p>\n",
    content_script: null,
    files: [
      {
        url: "/media/related/2025/e0f6f8.jpeg",
        thumbnail_url: "/media/related/2025/e0f6f8-thumb.webp",
        type: "image",
        name: "uxSbl.jpeg",
        description: "",
        fit: null,
      },
      {
        url: "/media/related/2025/2188b0.jpeg",
        thumbnail_url: "/media/related/2025/2188b0-thumb.webp",
        type: "image",
        name: "9ffkm.jpeg",
        description: "",
        fit: null,
      },
    ],
    is_preview: false,
  },
  {
    post_type: "app",
    title: "Treefactor",
    url: "/apps/webapp-treefactor/",
    is_published: true,
    published_at: "2024-10-09T12:41:16.434Z",
    theme: null,
    hero_embedded_url: null,
    hero_image: null,
    content_html: "<p></p>\n",
    content_script: null,
    files: [],
    is_preview: false,
  },
  {
    post_type: "changelog",
    title: "Microformats Reader 1.0.275",
    url: "/changelog/microformats-reader-1-0-275/",
    is_published: true,
    published_at: "2024-09-17T09:43:00Z",
    theme: null,
    hero_embedded_url: null,
    hero_image: null,
    content_html:
      "Many more microformat tags supported, now available for Firefox + Chrome.",
    content_script: null,
    files: [],
    is_preview: true,
  },
  {
    post_type: "post",
    title: null,
    url: "/posts/20240330e2f/",
    is_published: true,
    published_at: "2024-03-30T10:14:33Z",
    theme: null,
    hero_embedded_url: null,
    hero_image: null,
    content_html: "<p>The continuing saga of Holiday Cat</p>\n",
    content_script: null,
    files: [
      {
        url: "/media/related/2025/8a36f4.jpg",
        thumbnail_url: "/media/related/2025/8a36f4-thumb.webp",
        type: "image",
        name: "PXL_20240328_205909119.PORTRAIT.jpg",
        description: "",
        fit: null,
      },
    ],
    is_preview: false,
  },
  {
    post_type: "app",
    title: "Clocks",
    url: "/apps/webapp-clocks/",
    is_published: true,
    published_at: "2024-03-01T18:28:46.258Z",
    theme: null,
    hero_embedded_url: null,
    hero_image: null,
    content_html: "<p></p>\n",
    content_script: null,
    files: [],
    is_preview: false,
  },
  {
    post_type: "app",
    title: "Palette",
    url: "/apps/webapp-palette/",
    is_published: true,
    published_at: "2024-02-29T12:03:48.136Z",
    theme: null,
    hero_embedded_url: null,
    hero_image: null,
    content_html: "Simple viewer for a colour palette.",
    content_script: null,
    files: [],
    is_preview: true,
  },
  {
    post_type: "app",
    title: "Orbitals",
    url: "/apps/webapp-orbitals/",
    is_published: true,
    published_at: "2024-02-28T15:47:18.164Z",
    theme: null,
    hero_embedded_url: null,
    hero_image: null,
    content_html: "<p></p>\n",
    content_script: null,
    files: [],
    is_preview: false,
  },
  {
    post_type: "changelog",
    title: "django-wm 4.1.1",
    url: "/changelog/django-wm-4-1-1/",
    is_published: true,
    published_at: "2024-02-10T15:14:11Z",
    theme: null,
    hero_embedded_url: null,
    hero_image: null,
    content_html:
      "Added Webmention.has_been_read field and new settings for enabling webmentions depending on source/target domain.",
    content_script: null,
    files: [],
    is_preview: true,
  },
  {
    post_type: "changelog",
    title: "django-wm 4.0.4",
    url: "/changelog/django-wm-4-0-4/",
    is_published: true,
    published_at: "2024-02-02T15:13:22Z",
    theme: null,
    hero_embedded_url: null,
    hero_image: null,
    content_html: "Resolves #53: Compatibility with dependency mf2py>=2.0.",
    content_script: null,
    files: [],
    is_preview: true,
  },
  {
    post_type: "post",
    title: null,
    url: "/posts/2023121542a/",
    is_published: true,
    published_at: "2023-12-15T22:31:23Z",
    theme: null,
    hero_embedded_url: null,
    hero_image: null,
    content_html: "<p>Holiday cat, I guess</p>\n",
    content_script: null,
    files: [
      {
        url: "/media/related/2025/16f8f6.jpg",
        thumbnail_url: "/media/related/2025/16f8f6-thumb.webp",
        type: "image",
        name: "PXL_20231221_222657475.jpg",
        description: "",
        fit: null,
      },
    ],
    is_preview: false,
  },
  {
    post_type: "post",
    title: null,
    url: "/posts/2023103061f/",
    is_published: true,
    published_at: "2023-10-30T18:14:00Z",
    theme: null,
    hero_embedded_url: null,
    hero_image: null,
    content_html:
      '<p>3D printed cat with a hat made from old jeans.</p>\n\n<p>Model by Toonz Factory: <a href="https://www.thingiverse.com/thing:6236328" >thingiverse/6236328</a></p>\n',
    content_script: null,
    files: [
      {
        url: "/media/related/2025/fe7cae.jpg",
        thumbnail_url: "/media/related/2025/fe7cae-thumb.webp",
        type: "image",
        name: "jpeg",
        description: "",
        fit: null,
      },
    ],
    is_preview: false,
  },
  {
    post_type: "app",
    title: "beatonma.org",
    url: "/apps/beatonmaorg/",
    is_published: true,
    published_at: "2023-06-28T20:32:40Z",
    theme: {
      muted: "#131313",
      vibrant: "#E13255",
    },
    hero_embedded_url: null,
    hero_image: null,
    content_html: "This website",
    content_script: null,
    files: [],
    is_preview: true,
  },
  {
    post_type: "changelog",
    title: "django-wm 4.0.2",
    url: "/changelog/django-wm-4-0-2/",
    is_published: true,
    published_at: "2023-05-27T15:12:48Z",
    theme: null,
    hero_embedded_url: null,
    hero_image: null,
    content_html:
      "Resolves #50: broken search field on QuotableAdmin.\nAdded tests for admin pages to avoid that sort of thing happening again.\nMinor touch-ups for the admin pages.\nSource and target URL fields are now read-only.\nAdded appropriate search fields and list…",
    content_script: null,
    files: [],
    is_preview: true,
  },
  {
    post_type: "changelog",
    title: "django-wm 4.0.1",
    url: "/changelog/django-wm-4-0-1/",
    is_published: true,
    published_at: "2022-12-22T15:12:17Z",
    theme: null,
    hero_embedded_url: null,
    hero_image: null,
    content_html:
      "Added management command mentions_reverify [filters ...] [--all]\nAllows you to reprocess received Webmentions to see if they are still ‘live’.\nAccepts a space-separated list of field=value queryset filters, or --all to reprocess all of them.\nAdded ma…",
    content_script: null,
    files: [],
    is_preview: true,
  },
  {
    post_type: "changelog",
    title: "django-wm 4.0.0",
    url: "/changelog/django-wm-4-0-0/",
    is_published: true,
    published_at: "2022-11-25T15:11:35Z",
    theme: null,
    hero_embedded_url: null,
    hero_image: null,
    content_html:
      "This update alters fields on MentionableMixin so you will need to run makemigrations and migrate after upgrading!\r\nMentionableMixin:\r\nallow_outgoing_webmentions default now configurable via settings.WEBMENTIONS_ALLOW_OUTGOING_DEFAULT.\r\nRemoved slug fiel…",
    content_script: null,
    files: [],
    is_preview: true,
  },
  {
    post_type: "changelog",
    title: "django-wm 3.1.1",
    url: "/changelog/django-wm-3-1-1/",
    is_published: true,
    published_at: "2022-10-26T15:10:54Z",
    theme: null,
    hero_embedded_url: null,
    hero_image: null,
    content_html:
      "Fixes #43: outgoing webmention being resubmitted continuously.",
    content_script: null,
    files: [],
    is_preview: true,
  },
  {
    post_type: "changelog",
    title: "django-wm 3.1.0",
    url: "/changelog/django-wm-3-1-0/",
    is_published: true,
    published_at: "2022-10-06T15:09:43Z",
    theme: null,
    hero_embedded_url: null,
    hero_image: null,
    content_html:
      "Resolves #38: Revalidate target URLs when handling pending mentions\r\nShould be unnecessary generally (they are also validated at discovery time when parsed from HTML) but important if validation checks are updated.\r\nResolves #41: Find correct endpoint …",
    content_script: null,
    files: [],
    is_preview: true,
  },
  {
    post_type: "changelog",
    title: "django-wm 3.0.0",
    url: "/changelog/django-wm-3-0-0/",
    is_published: true,
    published_at: "2022-09-29T15:07:23Z",
    theme: null,
    hero_embedded_url: null,
    hero_image: null,
    content_html:
      "Upgrade warning\nIf upgrading from an older version please be aware of these changes:\nUnused MentionableMixin.allow_incoming_webmentions field has been removed.\nAny existing instances of PendingIncomingWebmention and PendingOutgoingContent will be del…",
    content_script: null,
    files: [],
    is_preview: true,
  },
  {
    post_type: "changelog",
    title: "beatonma.org 2.0",
    url: "/changelog/beatonma-org-2-0/",
    is_published: true,
    published_at: "2022-05-19T18:41:15Z",
    theme: null,
    hero_embedded_url: null,
    hero_image: null,
    content_html: "Fitter. Happier. More productive.",
    content_script: null,
    files: [],
    is_preview: true,
  },
  {
    post_type: "app",
    title: "Subcircuit Switcher",
    url: "/apps/webapp-subcircuit-switcher/",
    is_published: true,
    published_at: "2022-05-14T18:45:20.789Z",
    theme: null,
    hero_embedded_url: null,
    hero_image: null,
    content_html:
      "Simulation of a 4PDT switch for moving a subcircuit between two parent circuits.",
    content_script: null,
    files: [],
    is_preview: true,
  },
];

export const SampleGithub: ResponseOf<"/api/github/recent/"> = {
  events: [
    {
      type: "PushEvent",
      created_at: "2025-02-20T20:27:49Z",
      id: 46793519323,
      repository: {
        id: 188595195,
        name: "beatonma/snommoc",
        url: "https://github.com/beatonma/snommoc",
        license: null,
        description: "Data server for Commons app",
      },
      payload: [
        {
          sha: "9976ee5f94e08b9200c8ec1f42ff3f3feefc231d",
          message:
            "Added PartyTerritory model to store the union geometry of all constituencies currently held by a party.\n\nIntention: This is much easier to load and render than every individual constituency when zoomed out.\nTo do: load geometry for visible constituencies when zoomed in; implement culling of non-visible geometries",
          url: "https://github.com/beatonma/snommoc/commits/9976ee5f94e08b9200c8ec1f42ff3f3feefc231d",
        },
        {
          sha: "02341149d22c50399e6a95279dd3611bca870515",
          message: "<Map /> now able to show user location marker.",
          url: "https://github.com/beatonma/snommoc/commits/02341149d22c50399e6a95279dd3611bca870515",
        },
        {
          sha: "e7b05e5031f02ad55187dc29a30575309229241c",
          message:
            "Enabled ordering of constituencies by closeness to a given location.",
          url: "https://github.com/beatonma/snommoc/commits/e7b05e5031f02ad55187dc29a30575309229241c",
        },
        {
          sha: "9c262db3133f245d01ad47aaa29bedd4358454f7",
          message:
            "Restructured pagination and API fetch paradigm to make it easier to use in different contexts.\n\nIt is now significantly easier to pass custom (typesafe) queries/filters to pagination components.\nReduced boilerplate functions: previously had implementations for each (mostly single-use) endpoint.",
          url: "https://github.com/beatonma/snommoc/commits/9c262db3133f245d01ad47aaa29bedd4358454f7",
        },
        {
          sha: "504c52ee2f6eea6cdc63b88aee31a7d35ab88420",
          message: "Dependency updates",
          url: "https://github.com/beatonma/snommoc/commits/504c52ee2f6eea6cdc63b88aee31a7d35ab88420",
        },
        {
          sha: "50db1e90f7f52222fb6abad19b6a91ba3b03c1f5",
          message:
            "Removed party color workaround which is no longer needed with tailwind v4.",
          url: "https://github.com/beatonma/snommoc/commits/50db1e90f7f52222fb6abad19b6a91ba3b03c1f5",
        },
        {
          sha: "3bbcdb726c05bdc02392a751121a49081a4ca541",
          message: "Added `./manage jest` command for frontend tests",
          url: "https://github.com/beatonma/snommoc/commits/3bbcdb726c05bdc02392a751121a49081a4ca541",
        },
        {
          sha: "02a92b65e1a0159754d0fe8b0ae01cca57b660fa",
          message: "Minor refactor of `components/map`",
          url: "https://github.com/beatonma/snommoc/commits/02a92b65e1a0159754d0fe8b0ae01cca57b660fa",
        },
        {
          sha: "8729999d7d60d4539f76ea84af860b77a9bf83ea",
          message:
            "Added `fitToExtents` option. If false, adding an overlay layer does not affect the view position.",
          url: "https://github.com/beatonma/snommoc/commits/8729999d7d60d4539f76ea84af860b77a9bf83ea",
        },
        {
          sha: "07a115307dc4a19f60a80f758c2e1c1ced6e7564",
          message:
            "Improved map view.\n\nNational party territories are loaded as a background layer to provide color.\nConstituency boundaries are layered on top showing only their outlines.\nInaccuracies in the simplified constituency outlines are not so obvious as\nthe gaps between boundaries do not leave gaps in the background color.\n\nConstituencies are loaded using user location as the focus so nearby\nconstituencies load first. (Only if location permission is already allowed,\notherwise location of Parliament in London is used as the focus).",
          url: "https://github.com/beatonma/snommoc/commits/07a115307dc4a19f60a80f758c2e1c1ced6e7564",
        },
        {
          sha: "90604c56ce5a1f16746df88de55c1d3159a840ff",
          message: "Constituency is now highlighted when clicked.",
          url: "https://github.com/beatonma/snommoc/commits/90604c56ce5a1f16746df88de55c1d3159a840ff",
        },
        {
          sha: "92ca10996bc41a947c76bb07d2e51fbe3a65e8f8",
          message: "Delay map loading until location resolves.",
          url: "https://github.com/beatonma/snommoc/commits/92ca10996bc41a947c76bb07d2e51fbe3a65e8f8",
        },
        {
          sha: "3b882fe9a1c3c49ac1e19a2b1af28a3a04d9b7d0",
          message: "Multiple constituencies can now be selected at once.",
          url: "https://github.com/beatonma/snommoc/commits/3b882fe9a1c3c49ac1e19a2b1af28a3a04d9b7d0",
        },
        {
          sha: "7c2c10f6a996e4896bea8781b80c476387c7b54a",
          message:
            "Clicking on a party name in the color key now highlights all constituencies represented by that party.",
          url: "https://github.com/beatonma/snommoc/commits/7c2c10f6a996e4896bea8781b80c476387c7b54a",
        },
        {
          sha: "fe933c323cd596ddda0435e161ce5f9fdcadaca7",
          message: "Default sort parties by name.",
          url: "https://github.com/beatonma/snommoc/commits/fe933c323cd596ddda0435e161ce5f9fdcadaca7",
        },
        {
          sha: "4752adad49dc48170e115cd8cf8e03a203348715",
          message: "Minor refactor",
          url: "https://github.com/beatonma/snommoc/commits/4752adad49dc48170e115cd8cf8e03a203348715",
        },
        {
          sha: "aa78a4c40c0b963e27d743984bf8288bb0caa85c",
          message:
            "Light/dark color schemes now applied via @utility, reducing duplication of colors.",
          url: "https://github.com/beatonma/snommoc/commits/aa78a4c40c0b963e27d743984bf8288bb0caa85c",
        },
        {
          sha: "06ae2bd86533b1e5dbe4c356ff9ffaa8852d3399",
          message:
            "Fill color is now mixed with white instead of transparent to ensure decent visibility in dark mode.",
          url: "https://github.com/beatonma/snommoc/commits/06ae2bd86533b1e5dbe4c356ff9ffaa8852d3399",
        },
        {
          sha: "0d2bfc52dca7ce71956aefa9e09f0156618289e4",
          message: "Mobile map UI",
          url: "https://github.com/beatonma/snommoc/commits/0d2bfc52dca7ce71956aefa9e09f0156618289e4",
        },
        {
          sha: "f4121f5045631addb75bc4b16bfaedbd91894708",
          message: "Moved national map view to /maps/",
          url: "https://github.com/beatonma/snommoc/commits/f4121f5045631addb75bc4b16bfaedbd91894708",
        },
      ],
    },
    {
      type: "PushEvent",
      created_at: "2025-02-16T15:16:39Z",
      id: 46621374592,
      repository: {
        id: 483399730,
        name: "beatonma/whammy-arduino",
        url: "https://github.com/beatonma/whammy-arduino",
        license: "gpl-3.0",
        description:
          "An Arduino-based MIDI controller for the Digitech Whammy IV effects pedal.",
      },
      payload: [
        {
          sha: "c87b8848ed00b939c9c2f1e6c16b38f844eae899",
          message: "Changed default mode to MODE_WAVES",
          url: "https://github.com/beatonma/whammy-arduino/commits/c87b8848ed00b939c9c2f1e6c16b38f844eae899",
        },
      ],
    },
    {
      type: "PushEvent",
      created_at: "2025-02-07T19:26:05Z",
      id: 46351109605,
      repository: {
        id: 188595195,
        name: "beatonma/snommoc",
        url: "https://github.com/beatonma/snommoc",
        license: null,
        description: "Data server for Commons app",
      },
      payload: [
        {
          sha: "54dc0fff41eb9e09e35bd43ddc80daee1bb8fa2f",
          message:
            "Minor layout fix for button layouts when only an icon is provided.",
          url: "https://github.com/beatonma/snommoc/commits/54dc0fff41eb9e09e35bd43ddc80daee1bb8fa2f",
        },
        {
          sha: "f70e674dd8ca95dc4f04a2ad40370f1bd696021a",
          message: "TabLayout overflow fix.",
          url: "https://github.com/beatonma/snommoc/commits/f70e674dd8ca95dc4f04a2ad40370f1bd696021a",
        },
        {
          sha: "1e783b43215aac3510b1b81742511f31be82c738",
          message:
            "WindowInsets defined via `--spacing-edge`.\n\nApplies inline padding to keep content away from window edges.\nOnly applied once: `--spacing-edge` is set to zero once it\nhas been applied to a parent so using WindowInsets on a descendant\nwill not apply duplicate insets.",
          url: "https://github.com/beatonma/snommoc/commits/1e783b43215aac3510b1b81742511f31be82c738",
        },
        {
          sha: "3ce13464f36152b3d25220f5b34937ad10d7bf58",
          message:
            "Minor layout tweaks + add link to components preview dev page",
          url: "https://github.com/beatonma/snommoc/commits/3ce13464f36152b3d25220f5b34937ad10d7bf58",
        },
        {
          sha: "bbcdfe0cf131a4cee51812209e8194cc55abb6cf",
          message: "Initial value for `useRef`",
          url: "https://github.com/beatonma/snommoc/commits/bbcdfe0cf131a4cee51812209e8194cc55abb6cf",
        },
        {
          sha: "6b77b2e3bee5e42a5ae949720c2020a82e4c9d76",
          message:
            "Extracted `<Map />` component with `useMap()` hook to enable reuse.",
          url: "https://github.com/beatonma/snommoc/commits/6b77b2e3bee5e42a5ae949720c2020a82e4c9d76",
        },
        {
          sha: "4da38be556dab6ee4ad1e9acb8321d0de6496732",
          message: "Minor bug fixes",
          url: "https://github.com/beatonma/snommoc/commits/4da38be556dab6ee4ad1e9acb8321d0de6496732",
        },
        {
          sha: "f14690c832d34c6019b8950bc7054a9279a3ed63",
          message:
            "Fix: usernames used in tests were too long for username field",
          url: "https://github.com/beatonma/snommoc/commits/f14690c832d34c6019b8950bc7054a9279a3ed63",
        },
        {
          sha: "c9cb77dbe32e819cd0f3bc733c18d131818b0657",
          message:
            "Created experimental national view of all constituencies.\n\nNeeds significant optimisation - exploring GeoDjango next.",
          url: "https://github.com/beatonma/snommoc/commits/c9cb77dbe32e819cd0f3bc733c18d131818b0657",
        },
        {
          sha: "3934f37a05d018a2f91ef0de0ffae3822644e31a",
          message:
            "Enabled GeoDjango with PostGIS for handling constituency boundaries.\n\nSide effect: this means that running tests with sqlite3 no longer works.\n  Added `django_manage` service (run with `./manage shell`) for\n  in-environment management - running tests, updating migrations, etc.\n\n`/maps/` view is improved but still experimental.\n- `<NationalMap />` now shows constituency info on hover.\n- Performance is much better but still pretty slow to load everything.\n  Adding caching (redis?) may help. Also test with nginx+gzip.",
          url: "https://github.com/beatonma/snommoc/commits/3934f37a05d018a2f91ef0de0ffae3822644e31a",
        },
      ],
    },
    {
      type: "PushEvent",
      created_at: "2025-01-31T19:57:51Z",
      id: 46119208451,
      repository: {
        id: 188595195,
        name: "beatonma/snommoc",
        url: "https://github.com/beatonma/snommoc",
        license: null,
        description: "Data server for Commons app",
      },
      payload: [
        {
          sha: "53ffebfd19c21df4b65b0b5ab2a5ee9e51ceb673",
          message:
            'Added `RegisteredInterest.description_data` JSONField which contains semi-parsed content from `description`.\n\n{\n "table": A list of (title, value) tuples suitable for display in a table UI.\n "additional_values": list[str] of non-keyed content\n}',
          url: "https://github.com/beatonma/snommoc/commits/53ffebfd19c21df4b65b0b5ab2a5ee9e51ceb673",
        },
        {
          sha: "e656dc2f928a3c0e2599cb648525b6704bb35554",
          message:
            "Improved resolution of `RegisteredInterest.description_data`.\n\nDates related to the administration of interest registration are now parsed\nmore aggressively from the description and stored separately from other fields.\nThere are often many of these dates, they can be ambiguous or contradictory,\nand generally don't seem all that useful. We still keep track of them and make\nthem available, but doing this allows them to be hidden by default to reduce noise.",
          url: "https://github.com/beatonma/snommoc/commits/e656dc2f928a3c0e2599cb648525b6704bb35554",
        },
        {
          sha: "282a84683fe20bd8e369e363cba18fcea23fc382",
          message: "Verbose career sections now displayed in a `TabLayout`.",
          url: "https://github.com/beatonma/snommoc/commits/282a84683fe20bd8e369e363cba18fcea23fc382",
        },
        {
          sha: "4f6c11c8841d044d8965f2a8b2f54afc85e5116a",
          message:
            "Migrated to tailwind 4 and reworked theming system to suit.",
          url: "https://github.com/beatonma/snommoc/commits/4f6c11c8841d044d8965f2a8b2f54afc85e5116a",
        },
      ],
    },
    {
      type: "GollumEvent",
      created_at: "2025-01-30T17:35:50Z",
      id: 46077853228,
      repository: {
        id: 179150364,
        name: "beatonma/django-wm",
        url: "https://github.com/beatonma/django-wm",
        license: "gpl-3.0",
        description: "Automatic Webmention functionality for Django models",
      },
      payload: [
        {
          name: "Release-4.1.2",
          url: "https://github.com/beatonma/django-wm/wiki/Release-4.1.2",
          action: "created",
        },
      ],
    },
    {
      type: "GollumEvent",
      created_at: "2025-01-30T17:34:44Z",
      id: 46077817406,
      repository: {
        id: 179150364,
        name: "beatonma/django-wm",
        url: "https://github.com/beatonma/django-wm",
        license: "gpl-3.0",
        description: "Automatic Webmention functionality for Django models",
      },
      payload: [
        {
          name: "Releases",
          url: "https://github.com/beatonma/django-wm/wiki/Releases",
          action: "edited",
        },
      ],
    },
    {
      type: "IssuesEvent",
      created_at: "2025-01-30T17:33:46Z",
      id: 46077785835,
      repository: {
        id: 179150364,
        name: "beatonma/django-wm",
        url: "https://github.com/beatonma/django-wm",
        license: "gpl-3.0",
        description: "Automatic Webmention functionality for Django models",
      },
      payload: {
        number: 54,
        url: "https://github.com/beatonma/django-wm/issues/54",
        closed_at: "2025-01-30T17:33:45+00:00",
      },
    },
    {
      type: "CreateEvent",
      created_at: "2025-01-30T17:08:31Z",
      id: 46076896912,
      repository: {
        id: 179150364,
        name: "beatonma/django-wm",
        url: "https://github.com/beatonma/django-wm",
        license: "gpl-3.0",
        description: "Automatic Webmention functionality for Django models",
      },
      payload: {
        ref_type: "tag",
        ref: "4.1.2",
      },
    },
    {
      type: "PushEvent",
      created_at: "2025-01-30T17:07:20Z",
      id: 46076854964,
      repository: {
        id: 179150364,
        name: "beatonma/django-wm",
        url: "https://github.com/beatonma/django-wm",
        license: "gpl-3.0",
        description: "Automatic Webmention functionality for Django models",
      },
      payload: [
        {
          sha: "a92ffd50951a105714f40f7a6483540dfdf86592",
          message: "Update latest python version 3.12 -> 3.13.",
          url: "https://github.com/beatonma/django-wm/commits/a92ffd50951a105714f40f7a6483540dfdf86592",
        },
      ],
    },
    {
      type: "PushEvent",
      created_at: "2025-01-30T17:03:59Z",
      id: 46076734698,
      repository: {
        id: 179150364,
        name: "beatonma/django-wm",
        url: "https://github.com/beatonma/django-wm",
        license: "gpl-3.0",
        description: "Automatic Webmention functionality for Django models",
      },
      payload: [
        {
          sha: "f035f568c5ab4fbc9277a358b338979ebba5264a",
          message:
            "4.1.2 Fixed [#54](https://github.com/beatonma/django-wm/issues/54): Broken on `wagtail>=6.2`.",
          url: "https://github.com/beatonma/django-wm/commits/f035f568c5ab4fbc9277a358b338979ebba5264a",
        },
        {
          sha: "05e49a8d63f32d6190327ac88a40038272f7247f",
          message:
            "Lock Ubuntu version to 22.04 to allow continued testing with Python 3.7.",
          url: "https://github.com/beatonma/django-wm/commits/05e49a8d63f32d6190327ac88a40038272f7247f",
        },
        {
          sha: "b9a133867755ed76d71e3f18cef9ce0312fcd5f1",
          message: "Update latest python version 3.12 -> 3.13.",
          url: "https://github.com/beatonma/django-wm/commits/b9a133867755ed76d71e3f18cef9ce0312fcd5f1",
        },
        {
          sha: "2654ab514520078a37759adf8b51db88962ee75c",
          message: "Merge pull request #55 from beatonma/4.1.2\n\n4.1.2",
          url: "https://github.com/beatonma/django-wm/commits/2654ab514520078a37759adf8b51db88962ee75c",
        },
      ],
    },
    {
      type: "PullRequestEvent",
      created_at: "2025-01-30T17:03:58Z",
      id: 46076734033,
      repository: {
        id: 179150364,
        name: "beatonma/django-wm",
        url: "https://github.com/beatonma/django-wm",
        license: "gpl-3.0",
        description: "Automatic Webmention functionality for Django models",
      },
      payload: {
        number: 55,
        url: "https://github.com/beatonma/django-wm/pull/55",
        merged_at: "2025-01-30 17:03:57+00:00",
        additions_count: 22,
        deletions_count: 8,
        changed_files_count: 5,
      },
    },
    {
      type: "PushEvent",
      created_at: "2025-01-30T16:49:23Z",
      id: 46076195097,
      repository: {
        id: 179150364,
        name: "beatonma/django-wm",
        url: "https://github.com/beatonma/django-wm",
        license: "gpl-3.0",
        description: "Automatic Webmention functionality for Django models",
      },
      payload: [
        {
          sha: "b9a133867755ed76d71e3f18cef9ce0312fcd5f1",
          message: "Update latest python version 3.12 -> 3.13.",
          url: "https://github.com/beatonma/django-wm/commits/b9a133867755ed76d71e3f18cef9ce0312fcd5f1",
        },
      ],
    },
    {
      type: "PushEvent",
      created_at: "2025-01-30T16:30:39Z",
      id: 46075481804,
      repository: {
        id: 179150364,
        name: "beatonma/django-wm",
        url: "https://github.com/beatonma/django-wm",
        license: "gpl-3.0",
        description: "Automatic Webmention functionality for Django models",
      },
      payload: [
        {
          sha: "05e49a8d63f32d6190327ac88a40038272f7247f",
          message:
            "Lock Ubuntu version to 22.04 to allow continued testing with Python 3.7.",
          url: "https://github.com/beatonma/django-wm/commits/05e49a8d63f32d6190327ac88a40038272f7247f",
        },
      ],
    },
    {
      type: "CreateEvent",
      created_at: "2025-01-30T16:22:23Z",
      id: 46075157528,
      repository: {
        id: 179150364,
        name: "beatonma/django-wm",
        url: "https://github.com/beatonma/django-wm",
        license: "gpl-3.0",
        description: "Automatic Webmention functionality for Django models",
      },
      payload: {
        ref_type: "branch",
        ref: "4.1.2",
      },
    },
    {
      type: "PushEvent",
      created_at: "2023-03-27T10:58:04Z",
      id: 27999829329,
      repository: {
        id: 483399730,
        name: "beatonma/whammy-arduino",
        url: "https://github.com/beatonma/whammy-arduino",
        license: "gpl-3.0",
        description:
          "An Arduino-based MIDI controller for the Digitech Whammy IV effects pedal.",
      },
      payload: [
        {
          sha: "0cee90da75c45e9001f2e03a71e1ee2cc0b2e611",
          message:
            "Minor layout tweaks. Added png render in case of differences with fonts or whatever.",
          url: "https://github.com/beatonma/whammy-arduino/commits/0cee90da75c45e9001f2e03a71e1ee2cc0b2e611",
        },
      ],
    },
    {
      type: "PushEvent",
      created_at: "2023-03-27T10:36:14Z",
      id: 27999312691,
      repository: {
        id: 483399730,
        name: "beatonma/whammy-arduino",
        url: "https://github.com/beatonma/whammy-arduino",
        license: "gpl-3.0",
        description:
          "An Arduino-based MIDI controller for the Digitech Whammy IV effects pedal.",
      },
      payload: [
        {
          sha: "45859f57a690a0843bf276ed46e3fe95c98db358",
          message:
            "Added missing resistors to switch GND connections.\n\nAlso minor layout fixes.",
          url: "https://github.com/beatonma/whammy-arduino/commits/45859f57a690a0843bf276ed46e3fe95c98db358",
        },
      ],
    },
    {
      type: "PushEvent",
      created_at: "2023-03-26T15:43:55Z",
      id: 27984992917,
      repository: {
        id: 483399730,
        name: "beatonma/whammy-arduino",
        url: "https://github.com/beatonma/whammy-arduino",
        license: "gpl-3.0",
        description:
          "An Arduino-based MIDI controller for the Digitech Whammy IV effects pedal.",
      },
      payload: [
        {
          sha: "cb7508f038a4877b867b48c8444f2b69c778a7a3",
          message: "Update README.md\n\nAdded link to wiring diagram.",
          url: "https://github.com/beatonma/whammy-arduino/commits/cb7508f038a4877b867b48c8444f2b69c778a7a3",
        },
      ],
    },
    {
      type: "PushEvent",
      created_at: "2023-03-26T15:37:28Z",
      id: 27984944528,
      repository: {
        id: 483399730,
        name: "beatonma/whammy-arduino",
        url: "https://github.com/beatonma/whammy-arduino",
        license: "gpl-3.0",
        description:
          "An Arduino-based MIDI controller for the Digitech Whammy IV effects pedal.",
      },
      payload: [
        {
          sha: "ad0a2ad2898746a14851a10a2ed27aa431932198",
          message:
            "Added wiring diagram and updated config.h to match the same configuration.",
          url: "https://github.com/beatonma/whammy-arduino/commits/ad0a2ad2898746a14851a10a2ed27aa431932198",
        },
      ],
    },
    {
      type: "PrivateEventSummary",
      created_at: "2023-03-22T17:28:54Z",
      event_count: 5,
      change_count: 12,
      repository_count: 1,
    },
    {
      type: "PushEvent",
      created_at: "2023-03-10T19:14:08Z",
      id: 27642348866,
      repository: {
        id: 86626264,
        name: "beatonma/microformats-reader",
        url: "https://github.com/beatonma/microformats-reader",
        license: null,
        description:
          "A browser extension that brings the Indieweb to the surface.",
      },
      payload: [
        {
          sha: "0f29f48550dadb26bbd5b6c2c921145923c40f35",
          message: "h-feed updates",
          url: "https://github.com/beatonma/microformats-reader/commits/0f29f48550dadb26bbd5b6c2c921145923c40f35",
        },
        {
          sha: "823357af230c97e46498b83083ce74ae917ca461",
          message: "Filesystem restructure",
          url: "https://github.com/beatonma/microformats-reader/commits/823357af230c97e46498b83083ce74ae917ca461",
        },
        {
          sha: "4888bb897c70f3739af2438e04d03a1b6dcc6404",
          message: "Basic author component with expandable h-card.",
          url: "https://github.com/beatonma/microformats-reader/commits/4888bb897c70f3739af2438e04d03a1b6dcc6404",
        },
        {
          sha: "110c7e2cc82d38f4ffd8eb33f476db68400ad544",
          message:
            "Refactored scss.\n\nScss now collected via @use/@forward to single 'entrypoint': `app.scss`.\nThis is imported once in `popup.tsx`, creating a single global <style> in the final page.\n\nPreviously, importing files in the tsx module of use resulted in many <style> tags with a lot of duplication.",
          url: "https://github.com/beatonma/microformats-reader/commits/110c7e2cc82d38f4ffd8eb33f476db68400ad544",
        },
        {
          sha: "8f8f3590411ae3a5251501db86d74ab74ecd60b9",
          message:
            "Styling refactor.\n\nRemoved unused css theming variables.\nReplaced --accent with --vibrant and --muted variants.\nImplemented injectTheme() - groundwork for potentially using source webpage colours or photos for theming.",
          url: "https://github.com/beatonma/microformats-reader/commits/8f8f3590411ae3a5251501db86d74ab74ecd60b9",
        },
        {
          sha: "6baee7bb1f27a063ea00ae83070cde52e106ee7d",
          message: "Added Dialog element with scrim handling.",
          url: "https://github.com/beatonma/microformats-reader/commits/6baee7bb1f27a063ea00ae83070cde52e106ee7d",
        },
        {
          sha: "82213fa1abd2d7134cce88a1c4128db89710ffc4",
          message:
            "`nullable(obj, options)`: now accepts an options object.\n\noptions:\n requiredKeys: require all keys be present with non-empty values.\n requireAnyKey: require at least one key be present with non-empty value",
          url: "https://github.com/beatonma/microformats-reader/commits/82213fa1abd2d7134cce88a1c4128db89710ffc4",
        },
        {
          sha: "34ab39618097778452df2c4827cefdf168f446e3",
          message:
            "Standardised border styling with %border-left and consistent use of --border-radius-x vars.",
          url: "https://github.com/beatonma/microformats-reader/commits/34ab39618097778452df2c4827cefdf168f446e3",
        },
        {
          sha: "3ebedac7d4978b5c32d76fd27c5f51eea25511fc",
          message:
            "Removed <InlineGroup>, made obsolete by <Row> properties.\n\nAdded <Row> `spaced` property.\n- Applies column-gap with a standard value from RowSpace enum.\n- If defined with no explicit value, defaults to RowSpace.Normal -> `--space-1x` in css.",
          url: "https://github.com/beatonma/microformats-reader/commits/3ebedac7d4978b5c32d76fd27c5f51eea25511fc",
        },
        {
          sha: "20433dbbc2d6cc2cb9aa9b47585e43b610db3257",
          message:
            "Added `initEntrypoint` to standardise page react element loading while setting document `title` and `lang` attributes.",
          url: "https://github.com/beatonma/microformats-reader/commits/20433dbbc2d6cc2cb9aa9b47585e43b610db3257",
        },
        {
          sha: "f2d71dc3a9bba5bf359d3dd17d71e7b9daa93c27",
          message:
            "Current git hash now available as `AppConfig.version`. Created options UI stub.",
          url: "https://github.com/beatonma/microformats-reader/commits/f2d71dc3a9bba5bf359d3dd17d71e7b9daa93c27",
        },
        {
          sha: "0e04620a5e67717cab08f140a5e07b0fe6b6e0a1",
          message:
            "Added additional data from git.\n\n- Manifest version now derived from git commit count.\n- Added AppConfig fields `versionHash`, `versionDate`, `versionDescription`.",
          url: "https://github.com/beatonma/microformats-reader/commits/0e04620a5e67717cab08f140a5e07b0fe6b6e0a1",
        },
        {
          sha: "8e00425e36115e1a9348bb2a52f86d0a9107db35",
          message:
            "Refactored compat module, moved dev-patching of i18n to dev module.",
          url: "https://github.com/beatonma/microformats-reader/commits/8e00425e36115e1a9348bb2a52f86d0a9107db35",
        },
        {
          sha: "8338e86e61f73e34db360723e5d3939e51cc859e",
          message: "Removed unused service worker",
          url: "https://github.com/beatonma/microformats-reader/commits/8338e86e61f73e34db360723e5d3939e51cc859e",
        },
        {
          sha: "533f0d746486a648fc14942e547c59a64e861e58",
          message: "Renamed initEntrypoint -> initEntrypointUi",
          url: "https://github.com/beatonma/microformats-reader/commits/533f0d746486a648fc14942e547c59a64e861e58",
        },
        {
          sha: "0ade98247b3297d7c0c2b0b214859d6c20f16daf",
          message: "Implemented basic toolbar icon controls",
          url: "https://github.com/beatonma/microformats-reader/commits/0ade98247b3297d7c0c2b0b214859d6c20f16daf",
        },
        {
          sha: "752283075970f63562048bb9fd51a796f7658d95",
          message: "Minor fixes",
          url: "https://github.com/beatonma/microformats-reader/commits/752283075970f63562048bb9fd51a796f7658d95",
        },
        {
          sha: "8482caf0f559555de5a470195dd5ef828e96ddd3",
          message:
            "Moved parsing to content-script.ts so that the toolbar badge can be updated without needing to open the popup.",
          url: "https://github.com/beatonma/microformats-reader/commits/8482caf0f559555de5a470195dd5ef828e96ddd3",
        },
      ],
    },
    {
      type: "PushEvent",
      created_at: "2023-03-03T18:04:04Z",
      id: 27478467604,
      repository: {
        id: 86626264,
        name: "beatonma/microformats-reader",
        url: "https://github.com/beatonma/microformats-reader",
        license: null,
        description:
          "A browser extension that brings the Indieweb to the surface.",
      },
      payload: [
        {
          sha: "01af0b8b5d190cd8e7055d238342b54652c5d17f",
          message: "Minor refactor",
          url: "https://github.com/beatonma/microformats-reader/commits/01af0b8b5d190cd8e7055d238342b54652c5d17f",
        },
        {
          sha: "64fe7effe0b76c079c4ec6eb96231621ee14b78c",
          message: "Refactored <Property>, <PropertyRow>.",
          url: "https://github.com/beatonma/microformats-reader/commits/64fe7effe0b76c079c4ec6eb96231621ee14b78c",
        },
        {
          sha: "b205e966449903ce8bc96302176710bb4d0d19b0",
          message: "Refactored <Property>, <PropertyRow>.",
          url: "https://github.com/beatonma/microformats-reader/commits/b205e966449903ce8bc96302176710bb4d0d19b0",
        },
      ],
    },
    {
      type: "PushEvent",
      created_at: "2023-03-03T13:58:20Z",
      id: 27472690074,
      repository: {
        id: 86626264,
        name: "beatonma/microformats-reader",
        url: "https://github.com/beatonma/microformats-reader",
        license: null,
        description:
          "A browser extension that brings the Indieweb to the surface.",
      },
      payload: [
        {
          sha: "ee1a8558d141ec40841b6443b7246e0686f8fe52",
          message: "Minor optimisation",
          url: "https://github.com/beatonma/microformats-reader/commits/ee1a8558d141ec40841b6443b7246e0686f8fe52",
        },
        {
          sha: "c5924269ae4847e071adaeb457f25e0d7bbfd619",
          message:
            "Restructured parsing and display.\n\nParse functions are now strongly typed and simplified/deduplicated.\n\nParsed microformats now accept arrays for most fields instead of just taking the first value.\n - There are some exceptions to this, such as h-card images.\n\n<Property/>, <PropertyRow/> updated to display properties with multiple values.",
          url: "https://github.com/beatonma/microformats-reader/commits/c5924269ae4847e071adaeb457f25e0d7bbfd619",
        },
        {
          sha: "7742f9af6720555a318dad722ccaab1fbdcd33ea",
          message: "Added OptionsContext for app configuration.",
          url: "https://github.com/beatonma/microformats-reader/commits/7742f9af6720555a318dad722ccaab1fbdcd33ea",
        },
        {
          sha: "5e04fff734f8bcc2b4031131aca894dfc5b0dad9",
          message:
            "Restructured dev environment.\n\nNew entrypoint (`popup.dev.html` + `popup.dev.tsx`) for in-tab UI building.\n- Adds dev toolbar which allows choice of different sample HTML to use as data source.\n- Otherwise just wraps normal Popup UI.\n\nGlobal `AppConfig.isDebug` set by environment variable in `package.json` command.\n\nSome additional parsing logic to make sure empty components are not rendered.",
          url: "https://github.com/beatonma/microformats-reader/commits/5e04fff734f8bcc2b4031131aca894dfc5b0dad9",
        },
        {
          sha: "dbf8ca2a68831878ffb63fb6830419e243165b35",
          message: "Fallback to TextAvatar if photo fails to load.",
          url: "https://github.com/beatonma/microformats-reader/commits/dbf8ca2a68831878ffb63fb6830419e243165b35",
        },
        {
          sha: "b7ee3306b2277efedf04008e63589ffa107dca1f",
          message:
            "Restructured dev environment.\n\nNew entrypoint (popup.dev.html + popup.dev.tsx) for in-tab UI building.\nAdds dev toolbar which allows choice of different sample HTML to use as data source.\n\nGlobal AppConfig.debug set by `package.json` `dev` command.",
          url: "https://github.com/beatonma/microformats-reader/commits/b7ee3306b2277efedf04008e63589ffa107dca1f",
        },
        {
          sha: "1f88223c0e50908e2abef03f1713f6af80561aa7",
          message: "Show icon for organisation if jobTitle not available.",
          url: "https://github.com/beatonma/microformats-reader/commits/1f88223c0e50908e2abef03f1713f6af80561aa7",
        },
        {
          sha: "7c3a7dbced615ef2f39db57d81e648e6f0c79d2b",
          message:
            "Fixed image parsing when `alt` not available.\nProperty can now accept an Image instead of an icon.",
          url: "https://github.com/beatonma/microformats-reader/commits/7c3a7dbced615ef2f39db57d81e648e6f0c79d2b",
        },
        {
          sha: "8a8d2cb2109fe4ee87959a7a60f1d420d521d783",
          message: "Extracted ExpandableCard component from HCard for reuse.",
          url: "https://github.com/beatonma/microformats-reader/commits/8a8d2cb2109fe4ee87959a7a60f1d420d521d783",
        },
        {
          sha: "61c5b695d7e353d9de5aa1c794344ab58599b201",
          message:
            "ExpandCollapseLayout/Dropdown can no longer change state when it has no child nodes",
          url: "https://github.com/beatonma/microformats-reader/commits/61c5b695d7e353d9de5aa1c794344ab58599b201",
        },
        {
          sha: "38144c756fad03081afcdcc0f0a466fb89bd2269",
          message: "Refactor",
          url: "https://github.com/beatonma/microformats-reader/commits/38144c756fad03081afcdcc0f0a466fb89bd2269",
        },
        {
          sha: "fd3b982759ad106f270944ce98a6ab55083028d9",
          message:
            "Improved mocking of i18n.getMessage when running in test/dev environment.\n\nNow handles placeholder args correctly.",
          url: "https://github.com/beatonma/microformats-reader/commits/fd3b982759ad106f270944ce98a6ab55083028d9",
        },
        {
          sha: "9057200fd328708ce6b418fb6279eb4930e952d6",
          message: "Improved datetime formatting",
          url: "https://github.com/beatonma/microformats-reader/commits/9057200fd328708ce6b418fb6279eb4930e952d6",
        },
        {
          sha: "1087f07debbdbb79fffb316f957b641e7a41d543",
          message: "Moved `takeIfNotEmpty`",
          url: "https://github.com/beatonma/microformats-reader/commits/1087f07debbdbb79fffb316f957b641e7a41d543",
        },
        {
          sha: "f13888f18b20f1fcee473b910b0644f980834f08",
          message: "Improved datetime formatting",
          url: "https://github.com/beatonma/microformats-reader/commits/f13888f18b20f1fcee473b910b0644f980834f08",
        },
        {
          sha: "735404340faceb38b3b4835cb7ea755a0343609b",
          message:
            "`dt` elements are now parsed as Date objects immediately (previously deferred handling to UI elements).\n\n<Property> `displayValue` now accepts Date objects.",
          url: "https://github.com/beatonma/microformats-reader/commits/735404340faceb38b3b4835cb7ea755a0343609b",
        },
        {
          sha: "469b7026a4031020235ba93fabcca0a8295a1cf3",
          message:
            "Added tests for array and object util functions.\n\nnullable(obj) now accepts an optional list of keys that should be ignored\n- i.e. the result can be null even if those keys have non-null values.",
          url: "https://github.com/beatonma/microformats-reader/commits/469b7026a4031020235ba93fabcca0a8295a1cf3",
        },
        {
          sha: "098885d0409895fd6b9d4e4b9930998409123e65",
          message:
            "Introduced EmbeddedHCard interface.\n\nThis is the result of parsing a property that may be either a simple 'name' string, or a complex embedded hcard.",
          url: "https://github.com/beatonma/microformats-reader/commits/098885d0409895fd6b9d4e4b9930998409123e65",
        },
      ],
    },
    {
      type: "PrivateEventSummary",
      created_at: "2023-02-20T19:55:53Z",
      event_count: 4,
      change_count: 7,
      repository_count: 3,
    },
    {
      type: "PushEvent",
      created_at: "2023-02-11T15:19:30Z",
      id: 27025681363,
      repository: {
        id: 86626264,
        name: "beatonma/microformats-reader",
        url: "https://github.com/beatonma/microformats-reader",
        license: null,
        description:
          "A browser extension that brings the Indieweb to the surface.",
      },
      payload: [
        {
          sha: "2f7834b346e70fddaebc361fcbb06360a5702636",
          message: "Parsers are now async.",
          url: "https://github.com/beatonma/microformats-reader/commits/2f7834b346e70fddaebc361fcbb06360a5702636",
        },
        {
          sha: "b9c5b39550ff727cb534d136ccc7cad02cb68797",
          message: "Deleted unused files from original release.",
          url: "https://github.com/beatonma/microformats-reader/commits/b9c5b39550ff727cb534d136ccc7cad02cb68797",
        },
        {
          sha: "254a486f3b28309106d31e4bc744237444264aa8",
          message: "Updated tests for async parser.",
          url: "https://github.com/beatonma/microformats-reader/commits/254a486f3b28309106d31e4bc744237444264aa8",
        },
        {
          sha: "f1f46d70a5ab026c1f5abb43e6815138a3035b86",
          message: "Refactored for reusable CardLayout",
          url: "https://github.com/beatonma/microformats-reader/commits/f1f46d70a5ab026c1f5abb43e6815138a3035b86",
        },
        {
          sha: "c811009585c11193461c2dfa1d84c8c6fec77f56",
          message: "Refactored for reusable CardLayout",
          url: "https://github.com/beatonma/microformats-reader/commits/c811009585c11193461c2dfa1d84c8c6fec77f56",
        },
        {
          sha: "044054fc0f8b3934dbf725927d504ae2802222d9",
          message: "Test refactoring",
          url: "https://github.com/beatonma/microformats-reader/commits/044054fc0f8b3934dbf725927d504ae2802222d9",
        },
        {
          sha: "11040ab5533640295065e4fa4d23047e6144dcc0",
          message: "Checkpoint: Basic h-feed parse and rendering.",
          url: "https://github.com/beatonma/microformats-reader/commits/11040ab5533640295065e4fa4d23047e6144dcc0",
        },
        {
          sha: "cc575ab57e27ddc0e2f25fb542d18ae5e9bffe84",
          message: "Reinstated missing link to maps.",
          url: "https://github.com/beatonma/microformats-reader/commits/cc575ab57e27ddc0e2f25fb542d18ae5e9bffe84",
        },
        {
          sha: "e5751548131c94509305666c95a2f912252d5fbd",
          message: "Enabled typescript strict mode.",
          url: "https://github.com/beatonma/microformats-reader/commits/e5751548131c94509305666c95a2f912252d5fbd",
        },
        {
          sha: "15faa9e6620124ca31699dcc358ad8dd9a36bddc",
          message:
            "Split monolithic Microformats enum into more specific enums within Microformat namespace.\n\nThis allows us to have a function that only accepts `h-` property names, for example.\ne.g. Parse.getRootsOfType()",
          url: "https://github.com/beatonma/microformats-reader/commits/15faa9e6620124ca31699dcc358ad8dd9a36bddc",
        },
        {
          sha: "0e0d8bb0c789e7dc542c78741c54364282a197b7",
          message: "Added category and content",
          url: "https://github.com/beatonma/microformats-reader/commits/0e0d8bb0c789e7dc542c78741c54364282a197b7",
        },
      ],
    },
    {
      type: "PrivateEventSummary",
      created_at: "2023-01-31T20:42:50Z",
      event_count: 38,
      change_count: 73,
      repository_count: 2,
    },
    {
      type: "IssuesEvent",
      created_at: "2023-01-04T11:53:00Z",
      id: 26217039054,
      repository: {
        id: 179150364,
        name: "beatonma/django-wm",
        url: "https://github.com/beatonma/django-wm",
        license: "gpl-3.0",
        description: "Automatic Webmention functionality for Django models",
      },
      payload: {
        number: 45,
        url: "https://github.com/beatonma/django-wm/issues/45",
        closed_at: "2023-01-04 11:52:59+00:00",
      },
    },
  ],
};
