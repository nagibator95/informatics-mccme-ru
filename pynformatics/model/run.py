from sqlalchemy import (
    Column,
    ForeignKey,
    ForeignKeyConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.types import (
    DateTime,
    Integer,
    String,
)

from pynformatics.model.ejudge_run import EjudgeRun
from pynformatics.model.meta import Base
from pynformatics.models import DBSession
from pynformatics.utils.functions import attrs_to_dict
from pynformatics.utils.notify import notify_user


EJUDGE_COLUMNS = [
    'run_id',
    'contest_id',
    'run_uuid',
    'score',
    'status',
    'lang_id',
    'test_num',
    'create_time',
    'last_change_time',
]


class Run(Base):
    __table_args__ = (
        ForeignKeyConstraint(
            ['ej_run_id', 'ej_contest_id'],
            ['ejudge.runs.run_id', 'ejudge.runs.contest_id'],
        ),
        {'schema': 'pynformatics'},
    )
    __tablename__ = 'runs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('moodle.mdl_user.id'))
    problem_id = Column(Integer, ForeignKey('moodle.mdl_problems.id'))
    statement_id = Column(Integer, ForeignKey('moodle.mdl_statements.id'))
    score = Column(Integer)
    create_time = Column(DateTime)

    user = relationship('SimpleUser', backref='runs')
    problem = relationship('EjudgeProblem', backref='runs2')
    statement = relationship('Statement', backref='runs')

    # Поля скопированные из ejudge.runs
    ejudge_run_id = Column('ej_run_id', Integer)
    ejudge_contest_id = Column('ej_contest_id', Integer)
    ejudge_run_uuid = Column('ej_run_uuid', String)

    ejudge_score = Column('ej_score', Integer)
    ejudge_status = Column('ej_status', Integer)
    ejudge_language_id = Column('ej_lang_id', Integer)
    ejudge_test_num = Column('ej_test_num', Integer)

    ejudge_create_time = Column('ej_create_time', DateTime)
    ejudge_last_change_time = Column('ej_last_change_time', DateTime)

    ejudge_run = relationship('EjudgeRun', backref='run')

    def get_output_archive(self):
        if "output_archive" not in self.__dict__:
            self.output_archive = EjudgeArchiveReader(submit_path(output_path, self.contest_id, self.run_id))
        return self.output_archive

    def parsetests(self): #parse data from xml archive
        self.test_count = 0
        self.tests = {}
        self.judge_tests_info = {}
        self.status_string = None
        self.maxtime = None
        if self.xml:
            rep = self.xml.getElementsByTagName('testing-report')[0]
            self.tests_count = int(rep.getAttribute('run-tests'))
            self.status_string = rep.getAttribute('status')
            self.host = self.xml.getElementsByTagName('host')[0].firstChild.nodeValue
            try:
                self.compiler_output = self.xml.getElementsByTagName('compiler_output')[0].firstChild.nodeValue
            except:
                self.compiler_output = ""
            for node in self.xml.getElementsByTagName('test'):
                number = node.getAttribute('num')
                status = node.getAttribute('status')
                time = node.getAttribute('time')
                real_time = node.getAttribute('real-time')
                max_memory_used = node.getAttribute('max-memory-used')
                self.test_count += 1
                try:
                   time = int(time)
                except ValueError:
                   time = 0

                try:
                   real_time = int(real_time)
                except ValueError:
                   real_time = 0
                   
                test = {'status': status, 
                        'string_status': get_string_status(status), 
                        'real_time': real_time, 
                        'time': time,
                        'max_memory_used' : max_memory_used
                       }
                judge_info = {}
            
                for _type in ('input', 'output', 'correct', 'stderr', 'checker'):
                    lst = node.getElementsByTagName(_type)
                    if lst and lst[0].firstChild:
                        judge_info[_type] = lst[0].firstChild.nodeValue
                    else:
                        judge_info[_type] = ""

                if node.hasAttribute('term-signal'):
                    judge_info['term-signal'] = int(node.getAttribute('term-signal'))
                if node.hasAttribute('exit-code'):
                    judge_info['exit-code'] = int(node.getAttribute('exit-code'))

                self.judge_tests_info[number] = judge_info
                self.tests[number] = test
            try:
                #print([test['time'] for test in self.tests.values()] + [test['real_time'] for test in self.tests.values()])
                self.maxtime = max([test['time'] for test in self.tests.values()] + [test['real_time'] for test in self.tests.values()])
            except ValueError:
                pass

    @property
    def status(self):
        return self.ejudge_status

    @property
    def language_id(self):
        return self.ejudge_language_id

    @staticmethod
    def pick_ejudge_columns(ejudge_run):
        return {
            'ejudge_run_id': ejudge_run.run_id,
            'ejudge_contest_id': ejudge_run.contest_id,
            'ejudge_run_uuid': ejudge_run.run_uuid,
            'ejudge_score': ejudge_run.score,
            'ejudge_status': ejudge_run.status,
            'ejudge_language_id': ejudge_run.lang_id,
            'ejudge_test_num': ejudge_run.test_num,
            'ejudge_create_time': ejudge_run.create_time,
            'ejudge_last_change_time': ejudge_run.last_change_time,
        }
    
    def get_by(run_id, contest_id):
        try:
            return DBSession.query(Run).filter(Run.run_id == int(run_id)).filter(Run.contest_id == int(contest_id)).first()            
        except:
            return None

    @lazy      
    def _get_compilation_protocol(self): 
        filename = submit_path(protocols_path, self.contest_id, self.run_id)
        if filename:
            if os.path.isfile(filename):
                myopen = lambda x,y : open(x, y, encoding='utf-8')
            else:
                filename += '.gz'
                myopen = gzip.open
            try:
                xml_file = myopen(filename, 'r')
                try:
                    res = xml_file.read()
                    try:
                        res = res.decode('cp1251').encode('utf8')
                    except:
                        pass

                    try:
                        return str(res, encoding='UTF-8')
                    except TypeError:
                        try:
                            res = res.decode('cp1251').encode('utf8')
                        except Exception:
                            pass
                        return res
                except Exception as e:
                    return e
            except IOError as e:
                return e
        else:
            return ''
    
    @lazy      
    def _get_protocol(self): 
        filename = submit_path(protocols_path, self.contest_id, self.run_id)
#        return filename
        if filename != '':
            return get_protocol_from_file(filename)
        else:
            return '<a></a>'
            
    protocol = property(_get_protocol)
    compilation_protocol = property(_get_compilation_protocol)
    
    @lazy 
    def _get_tested_protocol_data(self):
        self.xml = xml.dom.minidom.parseString(str(self.protocol))
        self.parsetests()

    def _set_output_archive(self, val):
        self.output_archive = val

    tested_protocol = property(_get_tested_protocol_data)
    get_by = staticmethod(get_by)

    @staticmethod
    def from_ejudge_run(ejudge_run):
        run = Run(
            user=ejudge_run.user,
            problem=ejudge_run.problem,
            score=ejudge_run.score,
            **Run.pick_ejudge_columns(ejudge_run),
        )
        return run

    @staticmethod
    def sync(ejudge_run_id, ejudge_contest_id):
        ejudge_run = DBSession.query(EjudgeRun).filter_by(
            run_id=ejudge_run_id,
            contest_id=ejudge_contest_id
        ).first()
        if not ejudge_run:
            return

        run = DBSession.query(Run).filter_by(
            ejudge_run_id=ejudge_run_id,
            ejudge_contest_id=ejudge_contest_id,
        ).first()
        if run:
            run.score = ejudge_run.score
            for key, value in Run.pick_ejudge_columns(ejudge_run).items():
                setattr(run, key, value)
        else:
            run = Run.from_ejudge_run(ejudge_run)
            DBSession.add(run)

        return run

    def serialize(self, context, attributes=None):
        if attributes is None:
            attributes = (
                'id',
                'problem_id',
                'statement_id',
                'score',
                'status',
                'language_id',
                'create_time',
            )
        serialized = attrs_to_dict(self, *attributes)
        if 'create_time' in attributes:
            serialized['create_time'] = str(self.create_time)

        return serialized
