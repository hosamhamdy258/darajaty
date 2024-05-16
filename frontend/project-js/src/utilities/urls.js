function UrlFixer(paths) {
  paths.map((route) => {
    route.path = route.path.trim().toLowerCase().replace(/ /g, "-");

    return route;
  });
}

export default UrlFixer;
