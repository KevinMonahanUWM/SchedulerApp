from TAScheduler.models import TA, Section, Lab
from TAScheduler.view_methods.section_methods import SectionObj


class LabObj(SectionObj):
    database = None

    def __init__(self, lab_info):
        super().__init__()
        if type(lab_info) is not Lab:
            raise TypeError("Data passed to init method is not a member of the lab database class")
        elif not Section.objects.filter(section_id=lab_info.section.section_id).exists():
            raise TypeError("The lab object does not exist in the database")
        self.database = lab_info

    def getID(self):
        return self.database.section.section_id

    def getParentCourse(self):
        return self.database.section.course

    def getLabTAAsgmt(self):
        return self.database.ta

    def addTA(self, active_ta):
        if type(active_ta) is not TA:
            raise TypeError("Data passed to addTA method is not a TA")
        elif not TA.objects.filter(user=active_ta.user).exists():
            raise RuntimeError("The TA object does not exist in the database")
        elif self.database.ta is not None:
            raise RuntimeError("A TA already exists in lab")
        self.database.ta = active_ta
        self.database.save()

    def removeTA(self):
        if self.database.ta is None:
            raise RuntimeError("No TA to remove from lab")
        self.database.ta = None
        self.database.save()