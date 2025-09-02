import os
import re
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap

###############################################################################
# Parsing Logic
###############################################################################

def load_manifest(manifest_path):
    """
    Reads the manifest file and returns a list of SystemVerilog/Verilog file paths,
    ignoring empty lines and lines starting with '#'.
    """
    file_paths = []
    with open(manifest_path, 'r') as mf:
        for line in mf:
            line_stripped = line.strip()
            if not line_stripped or line_stripped.startswith('#'):
                continue
            file_paths.append(line_stripped)
    return file_paths

def remove_comments_and_join_lines(content):
    """
    Removes single-line (// ...) and block comments (/* ... */) from a multi-line string,
    then returns a cleaned single-line representation for easier regex processing.
    """
    # Remove block comments: /* ... */
    content_no_block = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    # Remove single-line comments: // ...
    content_no_single = re.sub(r'//.*', '', content_no_block)
    # Convert to single line
    one_line = " ".join(content_no_single.split())
    return one_line

def parse_sv_file(file_path):
    """
    Reads a single SystemVerilog/Verilog file, returns a dictionary:
      {
        "modules": {
          <moduleName>: {
             "parameters": [(paramName, defaultVal), ...],
             "submodules": [<submoduleTypeName>, ...]
          },
          ...
        }
      }
    """
    with open(file_path, 'r') as f:
        original_content = f.read()

    cleaned = remove_comments_and_join_lines(original_content)

    # Regex to find entire module blocks: module <name> #(...) optional, then up to endmodule
    module_block_pattern = re.compile(
        r'(module\s+(\w+)\s*(?:#\((.*?)\))?\s*\(?.*?\)\s*;)'  # Start of module decl
        r'(.*?)'                                             # Module body (non-greedy)
        r'(endmodule)',                                      # End of module
        re.IGNORECASE | re.DOTALL
    )

    # Regex for extracting "parameter XXX = YYY" from the param_block
    parameter_pattern = re.compile(
        r'parameter\s+(\w+)\s*=\s*([^,]+)', 
        re.IGNORECASE
    )

    # Regex for submodule instantiations
    instantiation_pattern = re.compile(
        r'(\w+)'             # (1) submodule type, e.g. "clock_manager"
        r'\s*(?:#\(.*?\))?'  # (2) optional #(...) block
        r'\s+(\w+)\s*'       # (3) instance name
        r'\(.*?\)'           # (4) port list in parentheses, lazy
        r'\s*;'              # (5) semicolon
        , re.IGNORECASE | re.DOTALL
    )

    file_info = {"modules": {}}

    # Find all module blocks
    for match in module_block_pattern.finditer(cleaned):
        module_name = match.group(2)
        param_block = match.group(3)
        module_body = match.group(4)

        # Extract parameters
        parameters = []
        if param_block:
            for p_match in parameter_pattern.finditer(param_block):
                p_name = p_match.group(1)
                p_value = p_match.group(2).strip()
                parameters.append((p_name, p_value))

        # Find submodules within the module body
        submodules = []
        for inst_match in instantiation_pattern.finditer(module_body):
            submodule_type = inst_match.group(1)
            submodules.append(submodule_type)

        file_info["modules"][module_name] = {
            "parameters": list(set(parameters)),
            # Sort submodules for each module
            "submodules": sorted(list(set(submodules))),
        }

    return file_info

def build_design_hierarchy(file_paths):
    """
    Build a dictionary for the entire design by parsing multiple files:
        {
          moduleName: {
            "parameters": [...],
            "submodules": [...]
          },
          ...
        }
    """
    design_info = {}
    for path in file_paths:
        file_dict = parse_sv_file(path)
        for m_name, m_data in file_dict["modules"].items():
            if m_name not in design_info:
                design_info[m_name] = {
                    "parameters": [],
                    "submodules": []
                }

            # Merge parameters:
            existing_param_dict = dict(design_info[m_name]["parameters"])
            new_param_dict = dict(m_data["parameters"])
            existing_param_dict.update(new_param_dict)
            merged_params = list(existing_param_dict.items())

            # Merge submodules (and sort them alphabetically)
            merged_subs = list(set(design_info[m_name]["submodules"] + m_data["submodules"]))
            merged_subs = sorted(merged_subs)

            design_info[m_name]["parameters"] = merged_params
            design_info[m_name]["submodules"] = merged_subs

    return design_info

###############################################################################
# Visualization / Interactivity
###############################################################################

def data_to_pixel_units(ax, width_data, height_data):
    bottom_left_disp = ax.transData.transform((0, 0))
    top_right_disp   = ax.transData.transform((width_data, height_data))
    pixel_width  = top_right_disp[0] - bottom_left_disp[0]
    pixel_height = top_right_disp[1] - bottom_left_disp[1]
    return pixel_width, pixel_height

def measure_text_in_pixels(text_string, ax, fig, fontsize):
    temp_text = ax.text(0, 0, text_string, fontsize=fontsize, alpha=0)
    fig.canvas.draw()
    bbox = temp_text.get_window_extent(renderer=fig.canvas.get_renderer())
    temp_text.remove()
    return bbox.width, bbox.height

def find_font_size_that_fits(text_string, ax, fig, desired_box_size_data, max_font=10, min_font=5):
    """
    Chooses a font size that lets 'text_string' fit inside a 'desired_box_size_data' x 'desired_box_size_data' region.
    """
    box_width_px, box_height_px = data_to_pixel_units(ax, desired_box_size_data, desired_box_size_data)
    font_size = max_font
    while font_size >= min_font:
        text_w_px, text_h_px = measure_text_in_pixels(text_string, ax, fig, font_size)
        # Require small margin
        if text_w_px + 5 <= box_width_px and text_h_px + 5 <= box_height_px:
            return font_size
        font_size -= 1
    return min_font

def show_hierarchy_interactive(design_dict, top_module, prev_available):
    """
    Displays a hierarchy diagram in full-screen mode:
      - A large square for 'top_module'
      - Multiple rows of smaller squares for each submodule type.
    """
    if top_module not in design_dict:
        return None

    module_info = design_dict[top_module]
    # Already stored in alphabetical order by build_design_hierarchy
    submodules = module_info["submodules"]

    fig, ax = plt.subplots()

    # Attempt full-screen
    manager = plt.get_current_fig_manager()
    try:
        manager.full_screen_toggle()
    except:
        try:
            manager.window.showMaximized()
        except:
            pass

    # Draw the top-level module box (12x12)
    top_width = 12
    top_height = 12
    top_rect = patches.Rectangle((0, 0), top_width, top_height, fill=False, linewidth=2)
    ax.add_patch(top_rect)

    # Show parameters if any
    param_str = ""
    if module_info["parameters"]:
        parts = []
        for (p_name, p_val) in module_info["parameters"]:
            parts.append(f"{p_name}={p_val}")
        param_str = " | " + ", ".join(parts)

    ax.text(0.5, top_height - 1, f"Top: {top_module}{param_str}", fontsize=12, weight='bold')

    # We'll place submodules in multiple rows inside the top module
    margin = 1.0               # margin around edges
    sub_size = 2.0             # each submodule square is 2x2 in data coords
    horiz_gap = 0.5            # horizontal gap between squares
    vert_gap = 0.5             # vertical gap between rows

    # Effective width available (minus left/right margins)
    available_width = top_width - 2*margin
    # How many squares fit in one row
    if sub_size + horiz_gap > 0:
        ncols = max(1, int(available_width // (sub_size + horiz_gap)))
    else:
        ncols = 1

    # Color gradient: light red -> light blue
    light_red = "#FF9999"
    light_blue = "#9999FF"
    color_map = LinearSegmentedColormap.from_list("custom_cmap", [light_red, light_blue])

    submodule_boxes = {}
    num_subs = len(submodules)
    # Avoid division by zero if no submodules
    max_idx = max(num_subs - 1, 1)

    for i, sub in enumerate(submodules):
        # Which row/column are we on?
        row = i // ncols
        col = i % ncols

        # Compute X/Y positions
        x_pos = margin + col * (sub_size + horiz_gap)
        # We stack rows from top to bottom
        y_pos = top_height - margin - (row+1)*sub_size - row*vert_gap

        # Keep submodules in a color gradient
        color_fraction = i / max_idx
        color = color_map(color_fraction)

        rect = patches.Rectangle((x_pos, y_pos), sub_size, sub_size,
                                 fill=True, edgecolor='black', facecolor=color)
        ax.add_patch(rect)

        # Fit the submodule type name inside
        best_font = find_font_size_that_fits(sub, ax, fig, sub_size, max_font=10, min_font=5)
        ax.text(x_pos + 0.1,
                y_pos + sub_size - 0.1,
                sub,
                fontsize=best_font,
                va='top',
                ha='left')

        submodule_boxes[sub] = (x_pos, y_pos, sub_size, sub_size)

    # Adjust axes
    ax.set_xlim(-1, top_width + 2)
    ax.set_ylim(-1, top_height + 2)
    ax.set_aspect('equal', 'box')
    ax.set_title("SystemVerilog Hierarchy (Hover / Click / Backspace)")

    # Tooltip
    tooltip = ax.text(0, 0, "", fontsize=9, color='blue', visible=False,
                      bbox=dict(facecolor='white', alpha=0.8, edgecolor='blue', boxstyle='round,pad=0.3'))

    clicked_submodule = None
    user_pressed_backspace = False

    def on_motion(event):
        if event.inaxes != ax:
            tooltip.set_visible(False)
            fig.canvas.draw_idle()
            return

        mx, my = event.xdata, event.ydata
        for sub_name, (sx, sy, w, h) in submodule_boxes.items():
            if sx <= mx <= sx + w and sy <= my <= sy + h:
                tooltip.set_text(sub_name)
                tooltip.set_position((mx + 0.1, my + 0.1))
                tooltip.set_visible(True)
                fig.canvas.draw_idle()
                return

        tooltip.set_visible(False)
        fig.canvas.draw_idle()

    def on_click(event):
        nonlocal clicked_submodule
        if event.inaxes != ax:
            return

        mx, my = event.xdata, event.ydata
        for sub_name, (sx, sy, w, h) in submodule_boxes.items():
            if sx <= mx <= sx + w and sy <= my <= sy + h:
                clicked_submodule = sub_name
                plt.close(fig)
                return

    def on_key(event):
        nonlocal user_pressed_backspace
        if event.key == 'backspace' and prev_available:
            user_pressed_backspace = True
            plt.close(fig)

    fig.canvas.mpl_connect('motion_notify_event', on_motion)
    fig.canvas.mpl_connect('button_press_event', on_click)
    fig.canvas.mpl_connect('key_press_event', on_key)

    plt.show()

    if user_pressed_backspace:
        return "##BACK##"
    return clicked_submodule

###############################################################################
# Main Entry
###############################################################################

def main():
    """
    1) Reads 'source_rtl' (manifest file) and 'module_name' (top-level) from environment variables.
    2) Parses all the SystemVerilog/Verilog files from the manifest into a single 'design_dict'.
    3) Interactively displays a hierarchy diagram for the chosen top-level module.
    """
    manifest_file = os.environ.get("source_rtl")
    initial_top = os.environ.get("module_name")

    if not manifest_file:
        print("Error: Environment variable 'source_rtl' is not set.")
        return
    if not initial_top:
        print("Error: Environment variable 'module_name' is not set.")
        return

    file_paths = load_manifest(manifest_file)
    design_dict = build_design_hierarchy(file_paths)

    stack = [initial_top]
    while stack:
        current_top = stack[-1]
        if current_top not in design_dict:
            print(f"Module '{current_top}' not found in the design. Exiting.")
            break

        prev_available = (len(stack) > 1)
        result = show_hierarchy_interactive(design_dict, current_top, prev_available)

        if result == "##BACK##":
            stack.pop()
            if not stack:
                print("No more modules to go back to. Exiting.")
                break
        elif result is None:
            print("User closed the diagram. Exiting.")
            break
        else:
            clicked_submodule = result
            if clicked_submodule in design_dict:
                stack.append(clicked_submodule)
            else:
                print(f"Submodule '{clicked_submodule}' not in dictionary; cannot drill down.")
                break

if __name__ == "__main__":
    main()
