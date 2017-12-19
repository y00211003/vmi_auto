#  See the License for the specific language governing permissions and
#  limitations under the License.

from robot.errors import DataError
from robot.model import SuiteVisitor
from robot.result import ExecutionResult
from robot.utils import get_error_message
import sys,os

class GatherResults(SuiteVisitor):

    def __init__(self):
	self.tests = {}

    def visit_test(self, test):
	if test.passed:
	    self.tests[test.name] = 'PASS'
        elif not test.passed:
	    self.tests[test.name] = 'FAIL'

    def visit_keyword(self, kw):
	pass


def gather_test_results(output):
    if output.upper() == 'NONE':
	return {}
    gatherer = GatherResults()
    try:
	ExecutionResult(output, include_keywords=False).suite.visit(gatherer)	
	if not gatherer.tests:
	    return []
    except:
	raise DataError("Collecting failed tests from '%s' failed: %s"
                        % (output, get_error_message()))
    return gatherer.tests

if __name__ == '__main__':

    output=sys.argv[1]
    result = gather_test_results(output)
    print result
    print len(result) 
    print len(filter(lambda x: result[x] == 'PASS' , result))
