# -*- coding: utf-8 -*-

from collections import OrderedDict
from unittest import TestCase
from unittest.mock import Mock, call, patch

from mlblocks.mlpipeline import MLPipeline


class TestMLPipline(TestCase):

    @patch('mlblocks.mlpipeline.LOGGER')
    @patch('mlblocks.mlpipeline.MLBlock')
    def test___init__(self, mlblock_mock, logger_mock):
        blocks = [Mock(), Mock(), Mock(), Mock()]
        mlblock_mock.side_effect = blocks

        primitives = [
            'a.primitive.Name',
            'a.primitive.Name',
            'another.primitive.Name',
            'another.primitive.Name',
        ]
        expected_primitives = primitives.copy()

        init_params = {
            'a.primitive.Name': {
                'an_argument': 'value',
            },
            'another.primitive.Name#2': {
                'another': 'argument_value',
            }
        }
        expected_init_params = init_params.copy()
        input_names = {
            'another.primitive.Name#1': {
                'a_name': 'another_name',
            }
        }
        expected_input_names = input_names.copy()

        mlpipeline = MLPipeline(primitives, init_params, input_names)

        assert mlpipeline.primitives == expected_primitives
        assert mlpipeline.init_params == expected_init_params
        assert mlpipeline.blocks == OrderedDict((
            ('a.primitive.Name#1', blocks[0]),
            ('a.primitive.Name#2', blocks[1]),
            ('another.primitive.Name#1', blocks[2]),
            ('another.primitive.Name#2', blocks[3])
        ))
        assert mlpipeline.input_names == expected_input_names
        assert mlpipeline.output_names == dict()
        assert mlpipeline._tunable_hyperparameters == {
            'a.primitive.Name#1': blocks[0].get_tunable_hyperparameters.return_value,
            'a.primitive.Name#2': blocks[1].get_tunable_hyperparameters.return_value,
            'another.primitive.Name#1': blocks[2].get_tunable_hyperparameters.return_value,
            'another.primitive.Name#2': blocks[3].get_tunable_hyperparameters.return_value
        }

        expected_calls = [
            call('a.primitive.Name', an_argument='value'),
            call('a.primitive.Name', an_argument='value'),
            call('another.primitive.Name'),
            call('another.primitive.Name', another='argument_value'),
        ]
        assert mlblock_mock.call_args_list == expected_calls

        logger_mock.warning.assert_called_once_with(
            'Non-numbered init_params are being used for more than one block %s.',
            'a.primitive.Name'
        )

    def test_get_tunable_hyperparameters(self):
        mlpipeline = MLPipeline(list())
        tunable = dict()
        mlpipeline._tunable_hyperparameters = tunable

        returned = mlpipeline.get_tunable_hyperparameters()

        assert returned == tunable
        assert returned is not tunable

    def test_get_hyperparameters(self):
        block_1 = Mock()
        block_2 = Mock()
        blocks = OrderedDict((
            ('a.primitive.Name#1', block_1),
            ('a.primitive.Name#2', block_2),
        ))
        mlpipeline = MLPipeline(list())
        mlpipeline.blocks = blocks

        hyperparameters = mlpipeline.get_hyperparameters()

        assert hyperparameters == {
            'a.primitive.Name#1': block_1.get_hyperparameters.return_value,
            'a.primitive.Name#2': block_2.get_hyperparameters.return_value,
        }
        block_1.get_hyperparameters.assert_called_once_with()
        block_2.get_hyperparameters.assert_called_once_with()

    def test_set_hyperparameters(self):
        block_1 = Mock()
        block_2 = Mock()
        blocks = OrderedDict((
            ('a.primitive.Name#1', block_1),
            ('a.primitive.Name#2', block_2),
        ))
        mlpipeline = MLPipeline(list())
        mlpipeline.blocks = blocks

        hyperparameters = {
            'a.primitive.Name#2': {
                'some': 'arg'
            }
        }
        mlpipeline.set_hyperparameters(hyperparameters)

        block_1.set_hyperparameters.assert_not_called()
        block_2.set_hyperparameters.assert_called_once_with({'some': 'arg'})

    def test__get_block_args(self):
        pass

    def test__get_outputs(self):
        pass

    def test_fit(self):
        pass

    def test_predict(self):
        pass

    def test_to_dict(self):
        pass

    def test_save(self):
        pass

    def test_from_dict(self):
        pass

    def test_load(self):
        pass
