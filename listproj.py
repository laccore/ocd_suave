import csv
import os

# projects_dir: root directory containing project dirs
def go(projects_dir):
    proj_paths = []
    for f in os.listdir(projects_dir):
        p = os.path.join(projects_dir, f)
        if not f.startswith('!') and os.path.isdir(p):
            proj_paths.append(p)
    print(proj_paths)

# proj_path: path to project dir
def get_project_images(proj_path):
    img_path = os.path.join(proj_path, "Images")
    images = []
    for f in os.listdir(images_path):
        pass # take only images with laccore names

# gather project name, metadata section names and other metadata from inventory file
# check project dir for matching images, ignoring -A/W, suffixes, etc
# report on % of matches, write to per-project log, also stdout and/or a unified log
# for each matching image, create row in SuAVE CSV

# return dict with (k=project name, v=list of project's section image names)
def read_inventory(inv_path):
    proj_data = {}
    with open(inv_path, encoding='utf-8-sig') as invfile:
        reader = csv.reader(invfile)
        for row in reader:
            name, section_name = row[0], row[8]
            if len(name) == 0:
                continue
            if name in proj_data:
                proj_data[name].append(section_name)
            else:
                proj_data[name] = [section_name]

        # print(f"Found {len(proj_data)} projects. {sorted(list(proj_data.keys()))[:10]}")
    return proj_data

# find images in vault that match section names in inventory file
def find_vault_images(proj_name, section_names, vault_path):
    proj_path = os.path.join(vault_path, proj_name)
    if not os.path.exists(proj_path):
        print(f"No project dir found for {proj_name}")
        return
    proj_img_path = os.path.join(proj_path, "Images")
    if not os.path.exists(proj_img_path):
        print(f"No Images dir found for {proj_name} in {proj_img_path}")
        return
    images = [f for f in os.listdir(proj_img_path) if not os.path.isdir(f) and has_image_extension(f)]
    matches = []
    for sn in section_names: # find image corresponding to section_name
        found = False
        for i in images:
            if i.startswith(sn):
                if len(sn) < len(i) and i[len(sn):][0] in ['.', '-', ' ']:
                    matches.append((sn, i))
                    found = True
                    break
        # if not found:
            # print(f"  No match for {sn}")

    print(f"{proj_name}: Found {round((len(matches)/len(section_names))*100.0, 1)}% ({len(matches)}/{len(section_names)}) inventory section names.")
    return matches

def has_image_extension(fname):
    for ext in ['.jpg', '.jpeg', '.gif', '.bmp', '.tif', '.tiff', '.png']:
        if fname.lower().endswith(ext):
            return True
    return False

if __name__ == "__main__":
    proj_data = read_inventory("data/Inventory_20200916.csv")
    count = 0
    for name in sorted(list(proj_data.keys())):
        # print(proj_data[name])
        section_names = proj_data[name]
        # for section_names in proj_data[name]:
        print(f"Searching contents of Vault for project '{name}' with {len(section_names)} inventory sections...")
        matches = find_vault_images(name, section_names, "/Volumes/Vault/projects")
        count += 1
        if count >= 100:
            break
