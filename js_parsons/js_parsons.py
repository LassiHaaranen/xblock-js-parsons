import pkg_resources
from lms_mixin import LmsCompatibilityMixin
from xblock.core import XBlock
from xblock.fields import Scope, String, Boolean,Integer,Float
from xblock.fragment import Fragment

class JSParsonsXBlock(XBlock, LmsCompatibilityMixin):
    """

    """
    instructions = String(
        help="The instructions to show to learners",
        default="Drag and drop the code blocks to form your solution",
        scope=Scope.settings)
    
    problem = String(
        help="The lines of code to be sorted", 
        default='def is_true(boolean_value):\n\tif boolean_value:\n\t\treturn True\n\treturn False\n\treturn true #distractor\n', 
        scope=Scope.settings)

    student_attempts = Integer(
        default=0,
        scope=Scope.user_state,
        help="Number of attempts the student has made")

    student_score = Float(
        help="student's score on this problem",
        values={"min": 0, "step": .1},
        default=0,
        scope=Scope.user_state)

    def student_view(self, context):
        """
        Player view, displayed to the student
        """
        html = self.resource_string('public/html/example.html')
        fragment = Fragment(html.format(self=self)) 

        #Uncomment the following line when using in xblock-sdk
        fragment.add_javascript_url('http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.18/jquery-ui.min.js')
        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/js/js-parsons/lib/underscore-min.js'))
        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/js/js-parsons/lib/lis.js'))
        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/js/js-parsons/parsons.js'))
        fragment.add_javascript(self.resource_string( 'public/js/example.js'))
        fragment.add_css_url(self.runtime.local_resource_url(self, 'public/js/js-parsons/parsons.css'))
        fragment.initialize_js('JSParsonsXBlock')
        return fragment

    def studio_view(self, context=None):
        html = self.resource_string("public/html/studio.html")
        fragment = Fragment(html.format(self=self))
        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/js/studio.js'))
        fragment.initialize_js("JSParsonsXBlockStudioEdit")
        return fragment

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    @XBlock.json_handler
    def save_problem_lines(self, data, suffix=''):
        self.problem = data.get("problem_lines", '') 

    @XBlock.json_handler
    def report_progress(self, data, suffix=''):
        #TODO: add log handling...
        self.student_attempts += 1
        tmp = {}        
        if len(data.get("feedback",0)) == 0: #submission is correct
            self.student_score = self.max_score()

            tmp = {
                'student_score': "{:0.1f}".format(self.student_score),
                'student_attempts': self.student_attempts
            }
        else:
            tmp = {
                'student_score': "{:0.1f}".format(self.student_score),
                'student_attempts': self.student_attempts
            }
        self.runtime.publish(self,
            'grade',
            {
                'value': self.student_score,
                'max_value': 1.0,                
            }
        )

        return tmp


    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("JSParsonsXBlock",
             """<vertical_demo>
                <js-parsons />
                </vertical_demo>

             """),
        ]

