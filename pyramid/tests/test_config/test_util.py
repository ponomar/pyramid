import unittest
from pyramid.compat import text_

class TestPredicateList(unittest.TestCase):

    def _makeOne(self):
        from pyramid.config.util import PredicateList
        from pyramid.config import predicates
        inst = PredicateList()
        for name, factory in (
            ('xhr', predicates.XHRPredicate),
            ('request_method', predicates.RequestMethodPredicate),
            ('path_info', predicates.PathInfoPredicate),
            ('request_param', predicates.RequestParamPredicate),
            ('header', predicates.HeaderPredicate),
            ('accept', predicates.AcceptPredicate),
            ('containment', predicates.ContainmentPredicate),
            ('request_type', predicates.RequestTypePredicate),
            ('match_param', predicates.MatchParamPredicate),
            ('custom', predicates.CustomPredicate),
            ('traverse', predicates.TraversePredicate),
            ):
            inst.add(name, factory)
        return inst

    def _callFUT(self, **kw):
        inst = self._makeOne()
        config = DummyConfigurator()
        return inst.make(config, **kw)

    def test_ordering_xhr_and_request_method_trump_only_containment(self):
        order1, _, _ = self._callFUT(xhr=True, request_method='GET')
        order2, _, _ = self._callFUT(containment=True)
        self.assertTrue(order1 < order2)

    def test_ordering_number_of_predicates(self):
        from pyramid.config.util import predvalseq
        order1, _, _ = self._callFUT(
            xhr='xhr',
            request_method='request_method',
            path_info='path_info',
            request_param='param',
            match_param='foo=bar',
            header='header',
            accept='accept',
            containment='containment',
            request_type='request_type',
            custom=predvalseq([DummyCustomPredicate()]),
            )
        order2, _, _ = self._callFUT(
            xhr='xhr',
            request_method='request_method',
            path_info='path_info',
            request_param='param',
            match_param='foo=bar',
            header='header',
            accept='accept',
            containment='containment',
            request_type='request_type',
            custom=predvalseq([DummyCustomPredicate()]),
            )
        order3, _, _ = self._callFUT(
            xhr='xhr',
            request_method='request_method',
            path_info='path_info',
            request_param='param',
            match_param='foo=bar',
            header='header',
            accept='accept',
            containment='containment',
            request_type='request_type',
            )
        order4, _, _ = self._callFUT(
            xhr='xhr',
            request_method='request_method',
            path_info='path_info',
            request_param='param',
            match_param='foo=bar',
            header='header',
            accept='accept',
            containment='containment',
            )
        order5, _, _ = self._callFUT(
            xhr='xhr',
            request_method='request_method',
            path_info='path_info',
            request_param='param',
            match_param='foo=bar',
            header='header',
            accept='accept',
            )
        order6, _, _ = self._callFUT(
            xhr='xhr',
            request_method='request_method',
            path_info='path_info',
            request_param='param',
            match_param='foo=bar',
            header='header',
            )
        order7, _, _ = self._callFUT(
            xhr='xhr',
            request_method='request_method',
            path_info='path_info',
            request_param='param',
            match_param='foo=bar',
            )
        order8, _, _ = self._callFUT(
            xhr='xhr',
            request_method='request_method',
            path_info='path_info',
            request_param='param',
            )
        order9, _, _ = self._callFUT(
            xhr='xhr',
            request_method='request_method',
            path_info='path_info',
            )
        order10, _, _ = self._callFUT(
            xhr='xhr',
            request_method='request_method',
            )
        order11, _, _ = self._callFUT(
            xhr='xhr',
            )
        order12, _, _ = self._callFUT(
            )
        self.assertEqual(order1, order2)
        self.assertTrue(order3 > order2)
        self.assertTrue(order4 > order3)
        self.assertTrue(order5 > order4)
        self.assertTrue(order6 > order5)
        self.assertTrue(order7 > order6)
        self.assertTrue(order8 > order7)
        self.assertTrue(order9 > order8)
        self.assertTrue(order10 > order9)
        self.assertTrue(order11 > order10)
        self.assertTrue(order12 > order10)

    def test_ordering_importance_of_predicates(self):
        from pyramid.config.util import predvalseq
        order1, _, _ = self._callFUT(
            xhr='xhr',
            )
        order2, _, _ = self._callFUT(
            request_method='request_method',
            )
        order3, _, _ = self._callFUT(
            path_info='path_info',
            )
        order4, _, _ = self._callFUT(
            request_param='param',
            )
        order5, _, _ = self._callFUT(
            header='header',
            )
        order6, _, _ = self._callFUT(
            accept='accept',
            )
        order7, _, _ = self._callFUT(
            containment='containment',
            )
        order8, _, _ = self._callFUT(
            request_type='request_type',
            )
        order9, _, _ = self._callFUT(
            match_param='foo=bar',
            )
        order10, _, _ = self._callFUT(
            custom=predvalseq([DummyCustomPredicate()]),
            )
        self.assertTrue(order1 > order2)
        self.assertTrue(order2 > order3)
        self.assertTrue(order3 > order4)
        self.assertTrue(order4 > order5)
        self.assertTrue(order5 > order6)
        self.assertTrue(order6 > order7)
        self.assertTrue(order7 > order8)
        self.assertTrue(order8 > order9)
        self.assertTrue(order9 > order10)

    def test_ordering_importance_and_number(self):
        from pyramid.config.util import predvalseq
        order1, _, _ = self._callFUT(
            xhr='xhr',
            request_method='request_method',
            )
        order2, _, _ = self._callFUT(
            custom=predvalseq([DummyCustomPredicate()]),
            )
        self.assertTrue(order1 < order2)

        order1, _, _ = self._callFUT(
            xhr='xhr',
            request_method='request_method',
            )
        order2, _, _ = self._callFUT(
            request_method='request_method',
            custom=predvalseq([DummyCustomPredicate()]),
            )
        self.assertTrue(order1 > order2)

        order1, _, _ = self._callFUT(
            xhr='xhr',
            request_method='request_method',
            path_info='path_info',
            )
        order2, _, _ = self._callFUT(
            request_method='request_method',
            custom=predvalseq([DummyCustomPredicate()]),
            )
        self.assertTrue(order1 < order2)

        order1, _, _ = self._callFUT(
            xhr='xhr',
            request_method='request_method',
            path_info='path_info',
            )
        order2, _, _ = self._callFUT(
            xhr='xhr',
            request_method='request_method',
            custom=predvalseq([DummyCustomPredicate()]),
            )
        self.assertTrue(order1 > order2)

    def test_different_custom_predicates_with_same_hash(self):
        from pyramid.config.util import predvalseq
        class PredicateWithHash(object):
            def __hash__(self):
                return 1
        a = PredicateWithHash()
        b = PredicateWithHash()
        _, _, a_phash = self._callFUT(custom=predvalseq([a]))
        _, _, b_phash = self._callFUT(custom=predvalseq([b]))
        self.assertEqual(a_phash, b_phash)

    def test_traverse_has_remainder_already(self):
        order, predicates, phash = self._callFUT(traverse='/1/:a/:b')
        self.assertEqual(len(predicates), 1)
        pred = predicates[0]
        info = {'traverse':'abc'}
        request = DummyRequest()
        result = pred(info, request)
        self.assertEqual(result, True)
        self.assertEqual(info, {'traverse':'abc'})

    def test_traverse_matches(self):
        order, predicates, phash = self._callFUT(traverse='/1/:a/:b')
        self.assertEqual(len(predicates), 1)
        pred = predicates[0]
        info = {'match':{'a':'a', 'b':'b'}}
        request = DummyRequest()
        result = pred(info, request)
        self.assertEqual(result, True)
        self.assertEqual(info, {'match':
                                {'a':'a', 'b':'b', 'traverse':('1', 'a', 'b')}})

    def test_traverse_matches_with_highorder_chars(self):
        order, predicates, phash = self._callFUT(
            traverse=text_(b'/La Pe\xc3\xb1a/{x}', 'utf-8'))
        self.assertEqual(len(predicates), 1)
        pred = predicates[0]
        info = {'match':{'x':text_(b'Qu\xc3\xa9bec', 'utf-8')}}
        request = DummyRequest()
        result = pred(info, request)
        self.assertEqual(result, True)
        self.assertEqual(
            info['match']['traverse'],
            (text_(b'La Pe\xc3\xb1a', 'utf-8'),
             text_(b'Qu\xc3\xa9bec', 'utf-8'))
             )

    def test_custom_predicates_can_affect_traversal(self):
        from pyramid.config.util import predvalseq
        def custom(info, request):
            m = info['match']
            m['dummy'] = 'foo'
            return True
        _, predicates, _ = self._callFUT(
            custom=predvalseq([custom]),
            traverse='/1/:dummy/:a')
        self.assertEqual(len(predicates), 2)
        info = {'match':{'a':'a'}}
        request = DummyRequest()
        self.assertTrue(all([p(info, request) for p in predicates]))
        self.assertEqual(info, {'match':
                                {'a':'a', 'dummy':'foo',
                                 'traverse':('1', 'foo', 'a')}})

    def test_predicate_text_is_correct(self):
        from pyramid.config.util import predvalseq
        _, predicates, _ = self._callFUT(
            xhr='xhr',
            request_method='request_method',
            path_info='path_info',
            request_param='param',
            header='header',
            accept='accept',
            containment='containment',
            request_type='request_type',
            custom=predvalseq(
                [
                    DummyCustomPredicate(),
                    DummyCustomPredicate.classmethod_predicate,
                    DummyCustomPredicate.classmethod_predicate_no_text,
                ]
            ),
            match_param='foo=bar')
        self.assertEqual(predicates[0].text(), 'xhr = True')
        self.assertEqual(predicates[1].text(),
                         "request_method = request_method")
        self.assertEqual(predicates[2].text(), 'path_info = path_info')
        self.assertEqual(predicates[3].text(), 'request_param param')
        self.assertEqual(predicates[4].text(), 'header header')
        self.assertEqual(predicates[5].text(), 'accept = accept')
        self.assertEqual(predicates[6].text(), 'containment = containment')
        self.assertEqual(predicates[7].text(), 'request_type = request_type')
        self.assertEqual(predicates[8].text(), "match_param foo=bar")
        self.assertEqual(predicates[9].text(), 'custom predicate')
        self.assertEqual(predicates[10].text(), 'classmethod predicate')
        self.assertTrue(predicates[11].text().startswith('custom predicate'))

    def test_match_param_from_string(self):
        _, predicates, _ = self._callFUT(match_param='foo=bar')
        request = DummyRequest()
        request.matchdict = {'foo':'bar', 'baz':'bum'}
        self.assertTrue(predicates[0](Dummy(), request))

    def test_match_param_from_string_fails(self):
        _, predicates, _ = self._callFUT(match_param='foo=bar')
        request = DummyRequest()
        request.matchdict = {'foo':'bum', 'baz':'bum'}
        self.assertFalse(predicates[0](Dummy(), request))

    def test_match_param_from_dict(self):
        _, predicates, _ = self._callFUT(match_param=('foo=bar','baz=bum'))
        request = DummyRequest()
        request.matchdict = {'foo':'bar', 'baz':'bum'}
        self.assertTrue(predicates[0](Dummy(), request))

    def test_match_param_from_dict_fails(self):
        _, predicates, _ = self._callFUT(match_param=('foo=bar','baz=bum'))
        request = DummyRequest()
        request.matchdict = {'foo':'bar', 'baz':'foo'}
        self.assertFalse(predicates[0](Dummy(), request))

    def test_request_method_sequence(self):
        _, predicates, _ = self._callFUT(request_method=('GET', 'HEAD'))
        request = DummyRequest()
        request.method = 'HEAD'
        self.assertTrue(predicates[0](Dummy(), request))
        request.method = 'GET'
        self.assertTrue(predicates[0](Dummy(), request))
        request.method = 'POST'
        self.assertFalse(predicates[0](Dummy(), request))

    def test_request_method_ordering_hashes_same(self):
        hash1, _, __= self._callFUT(request_method=('GET', 'HEAD'))
        hash2, _, __= self._callFUT(request_method=('HEAD', 'GET'))
        self.assertEqual(hash1, hash2)
        hash1, _, __= self._callFUT(request_method=('GET',))
        hash2, _, __= self._callFUT(request_method='GET')
        self.assertEqual(hash1, hash2)

    def test_unknown_predicate(self):
        from pyramid.exceptions import ConfigurationError
        self.assertRaises(ConfigurationError, self._callFUT, unknown=1)
        

class TestActionInfo(unittest.TestCase):
    def _getTargetClass(self):
        from pyramid.config.util import ActionInfo
        return ActionInfo
        
    def _makeOne(self, filename, lineno, function, linerepr):
        return self._getTargetClass()(filename, lineno, function, linerepr)

    def test_class_conforms(self):
        from zope.interface.verify import verifyClass
        from pyramid.interfaces import IActionInfo
        verifyClass(IActionInfo, self._getTargetClass())

    def test_instance_conforms(self):
        from zope.interface.verify import verifyObject
        from pyramid.interfaces import IActionInfo
        verifyObject(IActionInfo, self._makeOne('f', 0, 'f', 'f'))

    def test_ctor(self):
        inst = self._makeOne('filename', 10, 'function', 'src')
        self.assertEqual(inst.file, 'filename')
        self.assertEqual(inst.line, 10)
        self.assertEqual(inst.function, 'function')
        self.assertEqual(inst.src, 'src')

    def test___str__(self):
        inst = self._makeOne('filename', 0, 'function', '   linerepr  ')
        self.assertEqual(str(inst),
                         "Line 0 of file filename:\n       linerepr  ")

class DummyCustomPredicate(object):
    def __init__(self):
        self.__text__ = 'custom predicate'

    def classmethod_predicate(*args): pass
    classmethod_predicate.__text__ = 'classmethod predicate'
    classmethod_predicate = classmethod(classmethod_predicate)

    @classmethod
    def classmethod_predicate_no_text(*args): pass # pragma: no cover

class Dummy:
    pass

class DummyRequest:
    subpath = ()
    matchdict = None
    def __init__(self, environ=None):
        if environ is None:
            environ = {}
        self.environ = environ
        self.params = {}
        self.cookies = {}

class DummyConfigurator(object):
    def maybe_dotted(self, thing):
        return thing
    
