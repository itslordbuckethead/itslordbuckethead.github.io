class thumbsHelper:
    def __init__(self, company, limit=None, verbose=True, sizes=(200, 250), testing=True):
        self.verbose = verbose
        self.company = company
        self.testing = testing
        self.onserver = onserver()
        self.sbase = sbase
        self.sizes = sizes
        self.dfolder = get_destfolder(self.company)
        self.destfolder = 'sewingsub/patternimgs/' + self.dfolder if \
            onserver() else 'patternimgs/' + self.dfolder
        self.destimgs = get_destpaths(self.company)
        self.destimgcnt = len(self.destimgs)
        self.comdb = companyDB(company)
        self.patterncnt = self.comdb.count()
        self.limit = limit
        self.comdbtodo = self.comdb.limit(self.limit) if self.limit is not None else self.comdb
        self.nothumbsforpattern = []
        self.thumbsdone = []

    def buildThumbs(self):
        for self.item in self.comdbtodo:
            self.ipaths = [x for x in self.destimgs if self.item.pattern_id in x]
            if self.ipaths is not None and len(self.ipaths) >= 1:
                self.ipaths.sort()
                self.tothumb = random.choice(self.ipaths)
                self.startpath, self.endpath = os.path.splitext(self.tothumb)
                self.tname = self.tothumb.rsplit('/')[-1]
                self.thumbtemp = 'patternimgs/_thumbs/' + self.item.pattern_id + '.thumb' + self.endpath
                resize_and_crop(self.tothumb, self.thumbtemp, self.sizes)
                self.imgondb = ImageSet.get_or_none(ImageSet.url.endswith(self.tname))
                if self.imgondb:
                    self.imgondb.thumb = True
                    self.imgondb.save()
                    self.thumbsdone.append(self.tname)
                else:
                    imgw, imgh = check_image_size(self.tothumb)
                    iurl = self.sbase + f'patternimgs{self.dfolder}/' + self.tname
                    ImageSet.create(company=self.item.company, pid=self.item.pattern_id, width=imgw, height=imgh,
                                    url=iurl)
            else:
                self.nothumbsforpattern.append(self.item.pattern_id)
                print("Pattern had not images to do: {} - {}".format(self.item.pattern_id, self.tothumb))