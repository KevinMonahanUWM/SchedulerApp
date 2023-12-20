from TAScheduler.models import TA, Instructor, Lecture, Section
from TAScheduler.view_methods.section_methods import SectionObj


class LectureObj(SectionObj):
    database = None

    def __init__(self, lecture_info):
        super().__init__()
        if type(lecture_info) is not Lecture:
            raise TypeError("Data passed to init method is not a member of the lecture database class")
        elif not Section.objects.filter(section_id=lecture_info.section.section_id).exists():
            raise TypeError("The lecture object does not exist in the database")
        self.database = lecture_info

    def getID(self):
        return self.database.section.section_id

    def getParentCourse(self):
        return self.database.section.course

    def getLectureTAAsgmt(self):  # new
        return self.database.ta

    def addTA(self, active_ta):  # new
        if type(active_ta) is not TA:
            raise TypeError("Data passed to addTA method is not a TA")
        elif not TA.objects.filter(user=active_ta.user).exists():
            raise RuntimeError("The TA object does not exist in the database")
        elif self.database.ta is not None:
            raise RuntimeError("A TA already exists in lecture")
        self.database.ta = active_ta
        self.database.save()

    def getLecInstrAsmgt(self):
        return self.database.instructor

    def addInstr(self, active_instr):
        if type(active_instr) is not Instructor:
            raise TypeError("Data passed to addInstructor method is not a Instructor")
        elif not Instructor.objects.filter(user=active_instr.user).exists():
            raise RuntimeError("The Instructor object does not exist in the database")
        elif self.database.instructor is not None:
            raise RuntimeError("An Instructor already exists in lecture")
        self.database.instructor = active_instr
        self.database.save()

    def removeInstr(self):
        if self.database.instructor is None:
            raise RuntimeError("No instructor to remove from lecture")
        self.database.instructor = None
        self.database.save()

    def removeTA(self):  # new
        if self.database.ta is None:
            raise RuntimeError("No TA to remove from lecture")
        self.database.ta = None
        self.database.save()