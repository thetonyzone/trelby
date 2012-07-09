import config
import mypickle
import screenplay
import util

# manages auto completion information for a single script.
class AutoCompletion:
    def __init__(self):
        # type configs, key = line type, value = Type
        self.types = {}

        # element types
        t = Type(screenplay.SCENE)
        self.types[t.ti.lt] = t

        t = Type(screenplay.CHARACTER)
        self.types[t.ti.lt] = t

        t = Type(screenplay.TRANSITION)
        t.items = [
            "CUT TO:",
            "DISSOLVE TO:",
            "FADE IN:",
            "FADE OUT",
            "FADE TO BLACK",
            "MATCH CUT TO:",
            "FADE TO:",
            "JUMP CUT TO:",
            "BACK TO:",
            "SMASH CUT TO:"
            ]
        self.types[t.ti.lt] = t

        self.refresh()

    # load config from string 's'. does not throw any exceptions, silently
    # ignores any errors, and always leaves config in an ok state.
    def load(self, s):
        vals = mypickle.Vars.makeVals(s)

        for t in self.types.itervalues():
            t.load(vals, "AutoCompletion/")

        self.refresh()

    # save config into a string and return that.
    def save(self):
        s = ""

        for t in self.types.itervalues():
            s += t.save("AutoCompletion/")

        return s

    # fix up invalid values and uppercase everything.
    def refresh(self):
        for t in self.types.itervalues():
            tmp = []

            for v in t.items:
                v = util.upper(util.toInputStr(v)).strip()

                if len(v) > 0:
                    tmp.append(v)

            t.items = tmp

    # get type's Type, or None if it doesn't exist.
    def getType(self, lt):
        return self.types.get(lt)

# auto completion info for one element type
class Type:
    cvars = None

    def __init__(self, lt):

        # pointer to TypeInfo
        self.ti = config.lt2ti(lt)

        if not self.__class__.cvars:
            v = self.__class__.cvars = mypickle.Vars()

            v.addBool("enabled", True, "Enabled")
            v.addList("items", [], "Items",
                      mypickle.StrLatin1Var("", "", ""))

            v.makeDicts()

        self.__class__.cvars.setDefaults(self)

    def save(self, prefix):
        prefix += "%s/" % self.ti.name

        return self.cvars.save(prefix, self)

    def load(self, vals, prefix):
        prefix += "%s/" % self.ti.name

        self.cvars.load(vals, prefix, self)
