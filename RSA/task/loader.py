from random import randint, choice

flag = "Ararat{Unp4dd3d_R54}"
names = ["James", "Robert", "John", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles",
         "Christopher", "Daniel", "Matthew", "Anthony", "Mark", "Donald", "Steven", "Paul", "Andrew", "Joshua",
         "Kenneth", "Kevin", "Brian", "George", "Edward", "Ronald", "Timothy", "Jason", "Jeffrey", "Ryan", "Jacob",
         "Gary", "Nicholas", "Eric", "Jonathan", "Stephen", "Larry", "Justin", "Scott", "Brandon", "Benjamin", "Samuel",
         "Gregory", "Frank", "Alexander", "Raymond", "Patrick", "Jack", "Dennis", "Jerry", "Tyler", "Aaron", "Jose",
         "Adam", "Henry", "Nathan", "Douglas", "Zachary", "Peter", "Kyle", "Walter", "Ethan", "Jeremy", "Harold",
         "Keith", "Christian", "Roger", "Noah", "Gerald", "Carl", "Terry", "Sean", "Austin", "Arthur", "Lawrence",
         "Jesse", "Dylan", "Bryan", "Joe", "Jordan", "Billy", "Bruce", "Albert", "Willie", "Gabriel", "Logan", "Alan",
         "Juan", "Wayne", "Roy", "Ralph", "Randy", "Eugene", "Vincent", "Russell", "Elijah", "Louis", "Bobby", "Philip",
         "Johnny"]

colors = ["aliceblue", "antiquewhite", "aqua", "aquamarine", "azure", "beige", "bisque", "black", "blanchedalmond",
          "blue", "blueviolet", "brown", "burlywood", "cadetblue", "chartreuse", "chocolate", "coral", "cornflowerblue",
          "cornsilk", "crimson", "cyan", "darkblue", "darkcyan", "darkgoldenrod", "darkgray", "darkgreen", "darkgrey",
          "darkkhaki", "darkmagenta", "darkolivegreen", "darkorange", "darkorchid", "darkred", "darksalmon",
          "darkseagreen", "darkslateblue", "darkslategray", "darkslategrey", "darkturquoise", "darkviolet", "deeppink",
          "deepskyblue", "dimgray", "dimgrey", "dodgerblue", "firebrick", "floralwhite", "forestgreen", "fuchsia",
          "gainsboro", "ghostwhite", "gold", "goldenrod", "gray", "green", "greenyellow", "grey", "honeydew", "hotpink",
          "indianred", "indigo", "ivory", "khaki", "lavender", "lavenderblush", "lawngreen", "lemonchiffon",
          "lightblue", "lightcoral", "lightcyan", "lightgoldenrodyellow", "lightgray", "lightgreen", "lightgrey",
          "lightpink", "lightsalmon", "lightseagreen", "lightskyblue", "lightslategray", "lightslategrey",
          "lightsteelblue", "lightyellow", "lime", "limegreen", "linen", "magenta", "maroon", "mediumaquamarine",
          "mediumblue", "mediumorchid", "mediumpurple", "mediumseagreen", "mediumslateblue", "mediumspringgreen",
          "mediumturquoise", "mediumvioletred", "midnightblue", "mintcream", "mistyrose", "moccasin", "navajowhite",
          "navy", "oldlace", "olive", "olivedrab", "orange", "orangered", "orchid", "palegoldenrod", "palegreen",
          "paleturquoise", "palevioletred", "papayawhip", "peachpuff", "peru", "pink", "plum", "powderblue", "purple",
          "red", "rosybrown", "royalblue", "saddlebrown", "salmon", "sandybrown", "seagreen", "seashell", "sienna",
          "silver", "skyblue", "slateblue", "slategray", "slategrey", "snow", "springgreen", "steelblue", "tan", "teal",
          "thistle", "tomato", "turquoise", "violet", "wheat", "white", "whitesmoke", "yellow", "yellowgreen"]

words = ["also", "play", "small", "end", "put", "home", "read", "hand", "port", "large", "spell", "add", "even", "land",
         "here", "must", "big", "high", "such", "follow", "act", "why", "ask", "men", "change", "went", "light", "kind",
         "off", "need", "house", "picture", "try", "us", "again", "animal", "point", "mother", "world", "near", "build",
         "self", "earth", "father", "head", "stand", "own", "page", "should", "country", "found", "answer", "school",
         "grow", "study", "still", "learn", "plant", "cover", "food", "sun", "four", "between", "state", "keep", "eye",
         "never", "last", "let", "thought", "city", "tree", "cross", "farm", "hard", "start", "might", "story", "saw",
         "far", "sea", "draw", "left", "late", "run", "don't", "while", "press", "close", "night", "real", "life",
         "few", "north", "open", "seem", "together", "next", "white", "children", "begin", "got", "walk", "example",
         "ease", "paper", "group", "always", "music", "those", "both", "mark", "often", "letter", "until", "mile",
         "river", "car", "feet", "care", "second", "book", "carry", "took", "science", "eat", "room", "friend", "began",
         "idea", "fish", "mountain", "stop", "once", "base", "hear", "horse", "cut", "sure", "watch", "color", "face",
         "wood", "main", "enough", "plain", "girl", "usual", "young", "ready", "above", "ever", "red", "list", "though",
         "feel", "talk", "bird", "soon", "body", "dog", "family", "direct", "pose", "leave", "song", "measure", "door",
         "product", "black", "short", "numeral", "class", "wind", "question", "happen", "complete", "ship", "area",
         "half", "rock", "order", "fire", "south", "problem", "piece", "told", "knew", "pass", "since", "top", "whole",
         "king", "space", "heard", "best", "hour", "better", "true", "during", "hundred", "five", "remember", "step",
         "early", "hold", "west", "ground", "interest", "reach", "fast", "verb", "sing", "listen", "six", "table",
         "travel", "less", "morning", "ten", "simple", "several", "vowel", "toward", "war", "lay", "against", "pattern",
         "slow", "center", "love", "person", "money", "serve", "appear", "road", "map", "rain", "rule", "govern",
         "pull", "cold", "notice", "voice", "unit", "power", "town", "fine", "certain", "fly", "fall", "lead", "cry",
         "dark", "machine", "note", "wait", "plan", "figure", "star", "box", "noun", "field", "rest", "correct", "able",
         "pound", "done", "beauty", "drive", "stood", "contain", "front", "teach", "week", "final", "gave", "green",
         "oh", "quick", "develop", "ocean", "warm", "free", "minute", "strong", "special", "mind", "behind", "clear",
         "tail", "produce", "fact", "street", "inch", "multiply", "nothing", "course", "stay", "wheel", "full", "force",
         "blue", "object", "decide", "surface", "deep", "moon", "island", "foot", "system", "busy", "test", "record",
         "boat", "common", "gold", "possible", "plane", "stead", "dry", "wonder", "laugh", "thousand", "ago", "ran",
         "check", "game", "shape", "equate", "hot", "miss", "brought", "heat", "snow", "tire", "bring", "yes",
         "distant", "fill", "east", "paint", "language", "among", "grand", "ball", "yet", "wave", "drop", "heart", "am",
         "present", "heavy", "dance", "engine", "position", "arm", "wide", "sail", "material", "size", "vary", "settle",
         "speak", "weight", "general", "ice", "matter", "circle", "pair", "include", "divide", "syllable", "felt",
         "perhaps", "pick", "sudden", "count", "square", "reason", "length", "represent", "art", "subject", "region",
         "energy", "hunt", "probable", "bed", "brother", "egg", "ride", "cell", "believe", "fraction", "forest", "sit",
         "race", "window", "store", "summer", "train", "sleep", "prove", "lone", "leg", "exercise", "wall", "catch",
         "mount", "wish", "sky", "board", "joy", "winter", "sat", "written", "wild", "instrument", "kept", "glass",
         "grass", "cow", "job", "edge", "sign", "visit", "past", "soft", "fun", "bright", "gas", "weather", "month",
         "million", "bear", "finish", "happy", "hope", "flower", "clothe", "strange", "gone", "jump", "baby", "eight",
         "village", "meet", "root", "buy", "raise", "solve", "metal", "whether", "push", "seven", "paragraph", "third",
         "shall", "held", "hair", "describe", "cook", "floor", "either", "result", "burn", "hill", "safe", "cat",
         "century", "consider", "type", "law", "bit", "coast", "copy", "phrase", "silent", "tall", "sand", "soil",
         "roll", "temperature", "finger", "industry", "value", "fight", "lie", "beat", "excite", "natural", "view",
         "sense", "ear", "else", "quite", "broke", "case", "middle", "kill", "son", "lake", "moment", "scale", "loud",
         "spring", "observe", "child", "straight", "consonant", "nation", "dictionary", "milk", "speed", "method",
         "organ", "pay", "age", "section", "dress", "cloud", "surprise", "quiet", "stone", "tiny", "climb", "cool",
         "design", "poor", "lot", "experiment", "bottom", "key", "iron", "single", "stick", "flat", "twenty", "skin",
         "smile", "crease", "hole", "trade", "melody", "trip", "office", "receive", "row", "mouth", "exact", "symbol",
         "die", "least", "trouble", "shout", "except", "wrote", "seed", "tone", "join", "suggest", "clean", "break",
         "lady", "yard", "rise", "bad", "blow", "oil", "blood", "touch", "grew", "cent", "mix", "team", "wire", "cost",
         "lost", "brown", "wear", "garden", "equal", "sent", "choose", "fell", "fit", "flow", "fair", "bank", "collect",
         "save", "control", "decimal", "gentle", "woman", "captain", "practice", "separate", "difficult", "doctor",
         "please", "protect", "noon", "whose", "locate", "ring", "character", "insect", "caught", "period", "indicate",
         "radio", "spoke", "atom", "human", "history", "effect", "electric", "expect", "crop", "modern", "element",
         "hit", "student", "corner", "party", "supply", "bone", "rail", "imagine", "provide", "agree", "thus",
         "capital", "won't", "chair", "danger", "fruit", "rich", "thick", "soldier", "process", "operate", "guess",
         "necessary", "sharp", "wing", "create", "neighbor", "wash", "bat", "rather", "crowd", "corn", "compare",
         "poem", "string", "bell", "depend", "meat", "rub", "tube", "famous", "dollar", "stream", "fear", "sight",
         "thin", "triangle", "planet", "hurry", "chief", "colony", "clock", "mine", "tie", "enter", "major", "fresh",
         "search", "send", "yellow", "gun", "allow", "print", "dead", "spot", "desert", "suit", "current", "lift",
         "rose", "continue", "block", "chart", "hat", "sell", "success", "company", "subtract", "event", "particular",
         "deal", "swim", "term", "opposite", "wife", "shoe", "shoulder", "spread", "arrange", "camp", "invent",
         "cotton", "born", "determine", "quart", "nine", "truck", "noise", "level", "chance", "gather", "shop",
         "stretch", "throw", "shine", "property", "column", "molecule", "select", "wrong", "gray", "repeat", "require",
         "broad", "prepare", "salt", "nose", "plural", "anger", "claim", "continent", "oxygen", "sugar", "death",
         "pretty", "skill", "women", "season", "solution", "magnet", "silver", "thank", "branch", "match", "suffix",
         "especially", "fig", "afraid", "huge", "sister", "steel", "discuss", "forward", "similar", "guide",
         "experience", "score", "apple", "bought", "led", "pitch", "coat", "mass", "card", "band", "rope", "slip",
         "win", "dream", "evening", "condition"]


def generate_name():
    return choice(names) + str(randint(1, 10000))


def generate_phrase():
    seed = randint(1, 6)
    if seed == 1:
        return choice(["Sorry", "Excuse me", "Nope", "I am so sorry", "Nah"]) + ", " + choice(names)
    elif seed == 2:
        return choice(["I love", "I know", "My friend is", "Traitor is", "Find", "Shoot"]) + " " + choice(names)
    elif seed == 3:
        return choice(names) + " " + choice(["and", "or", "xor"]) + " " + choice(names) + " " + \
               choice(["is Love", "FOREVER", "are enemies", "know each other", "hate others", "are weird"])
    elif seed == 4:
        return choice(colors) + " " + choice(words) + " " + choice(names)
    elif seed == 5:
        return choice(colors) + " " + choice(colors) + " " + choice(colors) + " " + choice(colors)
    elif seed == 6:
        return choice(colors) + " " + choice(names) + choice(["!", "?", "."])


def load_data(rsa):
    phrases = {generate_name(): generate_phrase() for _ in range(randint(100, 200))}
    for name in phrases:
        phrases[name] = rsa.encrypt(phrases[name].encode())
    phrases[choice(list(phrases.keys()))] = rsa.encrypt(flag.encode())
    return phrases
