import os
import glob
import polib
import json


class GenerateTranslations():
    def __init__(self):
    
        print("Scanning for accomplishments:")
        accoms = {}
        collslist = os.listdir("accomplishments")
        for collection in collslist:
            colldir = os.path.join("accomplishments",collection)
            aboutFile = open(os.path.join(colldir,"ABOUT"), 'r')
            cfg = json.load(aboutFile)
            deflang = cfg["langdefault"]
            deflangdir = os.path.join(colldir,deflang)
            deflangdirlist = os.listdir(deflangdir)
            for item in deflangdirlist:
                itempath = os.path.join(deflangdir,item)
                if os.path.isdir(itempath):
                    dislist = os.listdir(itempath)
                    for accom in dislist:
                        accompath = os.path.join(itempath,accom)
                        accID = collection + "/" + accom[:-15]
                        print(" " + accID)
                        accoms[accID] = {'origfile' : accompath, 'inlangfile' : os.path.join(item,accom), 'coll' : collection}
                else:
                    accID = collection + "/" + item[:-15]
                    print(" " + accID)
                    accoms[accID] = {'origfile' : itempath,'inlangfile' : item, 'coll' : collection}
    
        self.pofiles = glob.glob("generated/po/*.po")

        for f in self.pofiles:
            langcode = os.path.split(f)[1].split(".")[0]
            popath = "generated/po/" + langcode + ".po"
            
            print("Opening: " + langcode + " at " + popath)
            
            self.currentpo = polib.pofile(popath)
                
            for accomID in accoms:
                collection = accoms[accomID]['coll']
                origfile = open(accoms[accomID]['origfile'], 'r')
                inlangfile = accoms[accomID]['inlangfile']
                langdir = os.path.join(os.path.join("accomplishments/", collection), langcode)
                if not os.path.exists(langdir):
                    os.makedirs(langdir)
                    
                print("...processing: " + accomID)
                self.masterconfig = json.load(origfile)
                #title = self.masterconfig.get("accomplishment", "title")
                self.outputconfig = {}

                self.outputconfig['title'] = self.process_field(accomID, "title")
                
                self.outputconfig['description'] = self.process_field(accomID, "description")
                
                if "collection" in self.masterconfig.keys():
                    print(self.masterconfig["collection"])
                    self.outputconfig["collection"] = self.masterconfig["collection"]
                
                if "category" in self.masterconfig.keys():
                    self.outputconfig["category"] = self.masterconfig["category"]

                if "needs-signing" in self.masterconfig.keys():
                    self.outputconfig["needs-signing"] = self.masterconfig["needs-signing"]
                
                if "needs-information" in self.masterconfig.keys():
                    self.outputconfig["needs-information"] = self.masterconfig["needs-information"]
                    
                if "icon" in self.masterconfig.keys():
                    self.outputconfig["icon"] = self.masterconfig["icon"]
                
                if "depends" in self.masterconfig.keys():
                    self.outputconfig["depends"] = self.masterconfig["depends"]

                if "author" in self.masterconfig.keys():
                    self.outputconfig["author"] = self.masterconfig["author"]

                # things that can be translated
                
                summary = self.process_field(accomID, "summary")
                self.outputconfig["summary"] = summary

                steps = self.process_field(accomID, "steps")
                self.outputconfig["steps"] = steps

                tips = self.process_field(accomID, "tips")
                self.outputconfig["tips"] = tips
                
                pitfalls = self.process_field(accomID, "pitfalls")
                self.outputconfig["pitfalls"] = pitfalls
                
                help = self.process_field(accomID, "help")
                self.outputconfig["help"] = help

                inlangfile_splitted = inlangfile.split("/")
                if len(inlangfile_splitted) == 2:
                    if not os.path.exists(os.path.join(langdir, inlangfile_splitted[0])):
                        os.makedirs(os.path.join(langdir, inlangfile_splitted[0]))
                path = os.path.join(langdir, inlangfile)

                for k in list(self.outputconfig.keys()):
                    if self.outputconfig[k] is None:
                        del(self.outputconfig[k])

                outfile = open(path, "w")
                json.dump(self.outputconfig, outfile, indent=2, ensure_ascii=False)
                outfile.close()
                
        print("Done.")

    def process_field(self, accomID, field):
        print(field)
        try:
            val = None
            final = None
            val = self.currentpo.find(accomID + "_" + field).msgstr.split("\r\n")
            
            while True:
                try:
                    val.remove("")
                except ValueError:
                    break
            final = ""
            
            for l in val:
                final = final + (l + "\n")
            
            # remove the final \n
            final = final.rstrip()
            
            if final == "":
                final = self.masterconfig[field]
            return final
        except:
            if field in self.masterconfig.keys():
                print("......" + field + " not found, using original translation.")
                content = self.masterconfig[field]
                return content.rstrip()

if __name__=="__main__":
    trans = GenerateTranslations()
