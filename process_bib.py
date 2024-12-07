from collections import OrderedDict
from pathlib import Path


MAX_AUTHORS = 1e12  # no et. al.s in dissertation
REMOVE_FIELDS = ["primaryclass", "editor"]

top_lines = [
    "@CONTROL{REVTEX42Control}\n",
    '@CONTROL{apsrev42Control,author="00",editor="1",pages="1",title="1",year="0"}"\n',
]

bib_files = OrderedDict()


def parse_entry(entry_lines):
    entry = {}
    try:
        entry_type_line = entry_lines[0]
        entry_type, entry_key = entry_type_line.split("{")
    except:
        print("Error in entry type line")
        print("Last entry before this:")
        print(entries[-1])
        print("Entry lines:")
        print(entry_lines)
        print(entry_type_line)
        raise

    entry["entrytype"] = entry_type.strip("@ ")
    entry["key"] = entry_key.split(",")[0].strip()

    for line in entry_lines[1:]:
        if "=" in line:
            tkey, tvalue = line.split("=", 1)
            if "sqrt" in tkey:
                entry[key.strip()] += " " + line.strip().strip(",")  # noqa: F823
            else:
                key = tkey.lower()
                value = tvalue
                entry[key.strip()] = value.strip().strip(",")
        else:
            entry[key.strip()] += " " + line.strip().strip(",")

    return entry


def process_entry(entry):
    """Processing to"""
    author_key = "author"

    # remove fields
    for field in REMOVE_FIELDS:
        if field in entry:
            if field == "editor":
                if author_key not in entry:
                    continue
            entry.pop(field)

    # change collaboration field to author
    if "collaboration" in entry:
        entry["author"] = '"{' + entry["collaboration"].strip('"{}') + ' Collaboration}"'
        entry.pop("collaboration")

    # manually do et al. for too many authors
    if author_key in entry:
        authors = entry[author_key].split(" and ")

        if len(authors) > MAX_AUTHORS:
            entry[author_key] = authors[0] + " and others"
            if entry[author_key][0] == "{":
                entry[author_key] += "}"
            elif entry[author_key][0] == '"':
                entry[author_key] += '"'

    # add missing archiveprefix
    if "eprint" in entry and "archiveprefix" not in entry:
        entry["archiveprefix"] = '"arXiv"'

    if entry["entrytype"] == "article":
        if "journal" not in entry:
            if "reportnumber" in entry and "CMS-PAS-" in entry["reportnumber"]:
                entry["entrytype"] = "techreport"
            elif "CMS-DP-" in entry["key"]:
                entry["entrytype"] = "techreport"
            else:
                print(entry)
                raise ValueError("Journal not found in article!")

    # change misc to techreport for CMS reports
    if entry["entrytype"] == "misc":
        if "reportnumber" in entry:
            if (
                "CMS-PAS-" in entry["reportnumber"]
                or "CMS-DP-" in entry["reportnumber"]
                or "CMS-TDR-" in entry["reportnumber"]
                or "CMS-CR-" in entry["reportnumber"]
            ):
                entry["entrytype"] = "techreport"

        elif "CMS-DP-" in entry["key"]:
            entry["entrytype"] = "techreport"
            entry["reportnumber"] = '"' + entry["key"] + '"'

    # need to add number and type for techreports to display properly
    if entry["entrytype"] == "techreport":
        if "reportnumber" in entry:
            if "number" not in entry:
                entry["number"] = entry["reportnumber"]

            if "type" not in entry:
                if "CMS-PAS-" in entry["reportnumber"]:
                    entry["type"] = '"CMS Physics Analysis Summary"'

                if "CMS-TDR-" in entry["reportnumber"]:
                    entry["type"] = '"CMS Technical Design Report"'

                if "CMS-CR-" in entry["reportnumber"]:
                    entry["type"] = '"CMS Conference Report"'

                if "CMS-DP-" in entry["reportnumber"]:
                    entry["type"] = '"CMS Detector Performance Note"'

                if "ATLAS-SOFT-PUB" in entry["reportnumber"]:
                    entry["type"] = '"ATLAS Software Public Note"'

                if "ATLAS-CONF" in entry["reportnumber"]:
                    entry["type"] = '"ATLAS Conference Note"'

    # add quotes and curly brackets to title for correct capitalization
    title = entry["title"].strip('"{}')
    if "{" not in title and "}" not in title:
        entry["title"] = f'"{{{title}}}"'

    return entry


# load all bib files
bib_files_lines = []
for file in Path("bibliographies").glob("*.bib"):
    print(file)
    if Path(file).stem in ["bibliography", "AN"]:
        continue

    with Path(file).open("r") as f:
        lines = f.readlines()
        bib_files_lines += lines

    bib_files[file] = len(lines)

# parse all the entries
entries = []  # list of dictionaries, each dictionary represents a bib entry
seen_entries = set()  # keep track of unique entries
seen_titles = {}  # keep track of unique titles

entry_lines = []
entry_started = False

counter = 0
fcounter = 0
j = 0

for line in bib_files_lines:
    line = line.strip()

    if line.startswith("@") and not entry_started:
        entry_started = True
        entry_type, entry_key = line.split("{")
        entry_lines.append(line)
    elif line == "}":
        entry_started = False
        entry = parse_entry(entry_lines)

        if entry["key"] not in seen_entries:
            try:
                title = entry["title"].lower().strip('{}"')
            except KeyError:
                print(f"\nTitle not found in entry: {entry['key']}")
                print("Skipping entry")
                raise

            if title in seen_titles:
                # print(f"\nDuplicate title found! {title}")
                # print(f'In "{list(bib_files.keys())[fcounter]}", line {counter}.')
                # print("Original entry:", seen_titles[title])
                # print(f"Skipping entry: {entry['key']}")
                # print("Replacing occurrences in text to original entry's keys:")
                # command = f"find chapters/ -type f -name \"*.tex\" -print0 | xargs -0 sed -i '' 's/{entry['key']}/{seen_titles[title]}/g'"
                # print(command)
                # result = subprocess.run(command, shell=True, capture_output=True, text=True)
                # print(result.stdout)
                # print(result.stderr)
                pass
            else:
                seen_titles[title] = entry["key"]
                try:
                    entry = process_entry(entry)
                except:
                    print(f'In "{list(bib_files.keys())[fcounter]}", line {counter}.')
                    raise
                seen_entries.add(entry["key"])
                entries.append(entry)

        entry_lines = []
    elif entry_started:
        entry_lines.append(line)

    counter += 1

    if counter > bib_files[list(bib_files.keys())[fcounter]]:
        counter = 0
        fcounter += 1


with Path("bibliography.bib").open("w", encoding="utf-8") as f:
    f.writelines(top_lines)
    f.write("\n")
    for entry in entries:
        f.write("@{}{{{},\n".format(entry["entrytype"], entry["key"]))
        for key, value in entry.items():
            if key not in ["entrytype", "key"]:
                f.write("\t{} = {},\n".format(key, value))
        f.write("}\n\n")


print("Processed bibliography!")
