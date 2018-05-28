import os


def safe_path_return(path):
    """Returns path only if file exists in file system.

    :param path: Path to be returned.
    :raises FileNotFoundError: When file doesn't exist.
    """
    if os.path.exists(path):
        return path
    else:
        raise FileNotFoundError(f"File {path} doesn't exist.")


def graph2dot(g, filename, directory="graphs"):
    """Saves given graph in dot format.

    :param g: Graph to be saved.
    :param filename: File name.
    :param directory: Destination directory, default value 'graphs'.
    :return: Path to the saved file.
    """
    dot_ext = ".dot"
    dot_path = os.path.join(directory, filename+dot_ext)
    g.write_dot(dot_path)
    return safe_path_return(dot_path)


def dot2svg(dot_path):
    """Converts dot file into svg using dot command from graphviz package.

    :param dot_path:
    :return: Path to created svg file.
    """
    svg_ext = ".svg"
    prefix, _ = os.path.splitext(dot_path)
    svg_path = prefix + svg_ext
    os.system(f"dot {dot_path} -Tsvg > {svg_path}")
    return safe_path_return(svg_path)


def show_svg(svg_path):
    """Shows svg file if in Jupyter environment.

    :param svg_path: Path to file which will be shown in notebook.
    """
    try:
        from IPython.display import SVG, display
        display(SVG(svg_path))
    except ImportError:
        print("Could not render SVG graphs outside Jupyter notebook.")


def preview_graph(g, name):
    """Preview graph in Jupyter notebook.

    :param g: Graph to be previewed.
    :param name: Svg filename to be used.
    """
    show_svg(dot2svg(graph2dot(g, name)))