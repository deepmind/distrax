# Copyright 2021 DeepMind Technologies Limited. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Tests for `gumbel.py`."""

from absl.testing import absltest
from absl.testing import parameterized

import chex
from distrax._src.distributions import gumbel
from distrax._src.utils import equivalence
import jax.numpy as jnp
import numpy as np

RTOL = 3e-2


class GumbelTest(equivalence.EquivalenceTest, parameterized.TestCase):

  def setUp(self):
    # pylint: disable=too-many-function-args
    super().setUp(gumbel.Gumbel)
    self.assertion_fn = lambda x, y: np.testing.assert_allclose(x, y, rtol=RTOL)

#   @parameterized.named_parameters(
#       ('1d std gumbel', (0, 1)),
#       ('2d std gumbel', (np.zeros(2), np.ones(2))),
#       ('rank 2 std gumbel', (np.zeros((3, 2)), np.ones((3, 2)))),
#       ('broadcasted loc', (0, np.ones(3))),
#       ('broadcasted scale', (np.ones(3), 1)),
#   )
#   def test_event_shape(self, distr_params):
#     super()._test_event_shape(distr_params, dict())

  @chex.all_variants
  @parameterized.named_parameters(
      ('1d std gumbel, no shape', (0, 1), ()),
      ('1d std gumbel, int shape', (0, 1), 1),
      ('1d std gumbel, 1-tuple shape', (0, 1), (1,)),
      ('1d std gumbel, 2-tuple shape', (0, 1), (2, 2)),
      ('2d std gumbel, no shape', (np.zeros(2), np.ones(2)), ()),
      ('2d std gumbel, int shape', ([0, 0], [1, 1]), 1),
      ('2d std gumbel, 1-tuple shape', (np.zeros(2), np.ones(2)), (1,)),
      ('2d std gumbel, 2-tuple shape', ([0, 0], [1, 1]), (2, 2)),
      ('rank 2 std normal, 2-tuple shape', (np.zeros((3, 2)), np.ones(
          (3, 2))), (2, 2)),
      ('broadcasted loc', (0, np.ones(3)), (2, 2)),
      ('broadcasted scale', (np.ones(3), 1), ()),
  )
  def test_sample_shape(self, distr_params, sample_shape):
    distr_params = (np.asarray(distr_params[0], dtype=np.float32),
                    np.asarray(distr_params[1], dtype=np.float32))
    super()._test_sample_shape(distr_params, dict(), sample_shape)

  @chex.all_variants
  @parameterized.named_parameters(
      ('float32', jnp.float32),
      ('float64', jnp.float64))
  def test_sample_dtype(self, dtype):
    dist = self.distrax_cls(
        loc=jnp.zeros((), dtype), scale=jnp.ones((), dtype))
    samples = self.variant(dist.sample)(seed=self.key)
    self.assertEqual(samples.dtype, dist.dtype)
    chex.assert_type(samples, dtype)

  @chex.all_variants
  @parameterized.named_parameters(
      ('1d std gumbel, no shape', (0, 1), ()),
      ('1d std gumbel, int shape', (0, 1), 1),
      ('1d std gumbel, 1-tuple shape', (0, 1), (1,)),
      ('1d std gumbel, 2-tuple shape', (0, 1), (2, 2)),
      ('2d std gumbel, no shape', (np.zeros(2), np.ones(2)), ()),
      ('2d std gumbel, int shape', ([0, 0], [1, 1]), 1),
      ('2d std gumbel, 1-tuple shape', (np.zeros(2), np.ones(2)), (1,)),
      ('2d std gumbel, 2-tuple shape', ([0, 0], [1, 1]), (2, 2)),
      ('rank 2 std normal, 2-tuple shape', (np.zeros((3, 2)), np.ones(
          (3, 2))), (2, 2)),
      ('broadcasted loc', (0, np.ones(3)), (2, 2)),
      ('broadcasted scale', (np.ones(3), 1), ()),
  )
  def test_sample_and_log_prob(self, distr_params, sample_shape):
    distr_params = (np.asarray(distr_params[0], dtype=np.float32),
                    np.asarray(distr_params[1], dtype=np.float32))
    super()._test_sample_and_log_prob(
        dist_args=distr_params,
        dist_kwargs=dict(),
        sample_shape=sample_shape,
        assertion_fn=self.assertion_fn)

  @chex.all_variants
  @parameterized.named_parameters(
      ('1d dist, 1d value', (0, 1), 1),
      ('1d dist, 2d value', (0.5, 0.1), np.array([1, 2])),
      ('1d dist, 2d value as list', (0.5, 0.1), [1, 2]),
      ('2d dist, 1d value', (0.5 + np.zeros(2), 0.3 * np.ones(2)), 1),
      ('2d broadcasted dist, 1d value', (np.zeros(2), 0.8), 1),
      ('2d dist, 2d value', ([0.1, -0.5], 0.9 * np.ones(2)), np.array([1, 2])),
      ('1d dist, 1d value, edge case', (0, 1), 200),
  )
  def test_log_prob(self, distr_params, value):
    distr_params = (np.asarray(distr_params[0], dtype=np.float32),
                    np.asarray(distr_params[1], dtype=np.float32))
    value = np.asarray(value, dtype=np.float32)
    super()._test_attribute(
        attribute_string='log_prob',
        dist_args=distr_params,
        call_args=(value,),
        assertion_fn=self.assertion_fn)

  @chex.all_variants
  @parameterized.named_parameters(
      ('1d dist, 1d value', (0, 1), 1),
      ('1d dist, 2d value', (0.5, 0.1), np.array([1, 2])),
      ('1d dist, 2d value as list', (0.5, 0.1), [1, 2]),
      ('2d dist, 1d value', (0.5 + np.zeros(2), 0.3 * np.ones(2)), 1),
      ('2d broadcasted dist, 1d value', (np.zeros(2), 0.8), 1),
      ('2d dist, 2d value', ([0.1, -0.5], 0.9 * np.ones(2)), np.array([1, 2])),
      ('1d dist, 1d value, edge case', (0, 1), 200),
  )
  def test_prob(self, distr_params, value):
    distr_params = (np.asarray(distr_params[0], dtype=np.float32),
                    np.asarray(distr_params[1], dtype=np.float32))
    value = np.asarray(value, dtype=np.float32)
    super()._test_attribute(
        attribute_string='prob',
        dist_args=distr_params,
        call_args=(value,),
        assertion_fn=self.assertion_fn)

  @chex.all_variants
  @parameterized.named_parameters(
      ('1d dist, 1d value', (0, 1), 1),
      ('1d dist, 2d value', (0.5, 0.1), np.array([1, 2])),
      ('1d dist, 2d value as list', (0.5, 0.1), [1, 2]),
      ('2d dist, 1d value', (0.5 + np.zeros(2), 0.3 * np.ones(2)), 1),
      ('2d broadcasted dist, 1d value', (np.zeros(2), 0.8), 1),
      ('2d dist, 2d value', ([0.1, -0.5], 0.9 * np.ones(2)), np.array([1, 2])),
      ('1d dist, 1d value, edge case', (0, 1), 200),
  )
  def test_cdf(self, distr_params, value):
    distr_params = (np.asarray(distr_params[0], dtype=np.float32),
                    np.asarray(distr_params[1], dtype=np.float32))
    value = np.asarray(value, dtype=np.float32)
    super()._test_attribute(
        attribute_string='cdf',
        dist_args=distr_params,
        call_args=(value,),
        assertion_fn=self.assertion_fn)

  @chex.all_variants
  @parameterized.named_parameters(
      ('1d dist, 1d value', (0, 1), 1),
      ('1d dist, 2d value', (0.5, 0.1), np.array([1, 2])),
      ('1d dist, 2d value as list', (0.5, 0.1), [1, 2]),
      ('2d dist, 1d value', (0.5 + np.zeros(2), 0.3 * np.ones(2)), 1),
      ('2d broadcasted dist, 1d value', (np.zeros(2), 0.8), 1),
      ('2d dist, 2d value', ([0.1, -0.5], 0.9 * np.ones(2)), np.array([1, 2])),
      ('1d dist, 1d value, edge case', (0, 1), 200),
  )
  def test_log_cdf(self, distr_params, value):
    distr_params = (np.asarray(distr_params[0], dtype=np.float32),
                    np.asarray(distr_params[1], dtype=np.float32))
    value = np.asarray(value, dtype=np.float32)
    super()._test_attribute(
        attribute_string='log_cdf',
        dist_args=distr_params,
        call_args=(value,),
        assertion_fn=self.assertion_fn)

  @chex.all_variants(with_pmap=False)
  @parameterized.named_parameters(
      ('entropy', ([0., 1., -0.5], [0.5, 1., 1.5]), 'entropy'),
      ('entropy broadcasted loc', (0.5, [0.5, 1., 1.5]), 'entropy'),
      ('entropy broadcasted scale', ([0., 1., -0.5], 0.8), 'entropy'),
      ('mean', ([0., 1., -0.5], [0.5, 1., 1.5]), 'mean'),
      ('mean broadcasted loc', (0.5, [0.5, 1., 1.5]), 'mean'),
      ('mean broadcasted scale', ([0., 1., -0.5], 0.8), 'mean'),
      ('variance', ([0., 1., -0.5], [0.5, 1., 1.5]), 'variance'),
      ('variance broadcasted loc', (0.5, [0.5, 1., 1.5]), 'variance'),
      ('variance broadcasted scale', ([0., 1., -0.5], 0.8), 'variance'),
      ('stddev', ([0., 1., -0.5], [0.5, 1., 1.5]), 'stddev'),
      ('stddev broadcasted loc', (0.5, [0.5, 1., 1.5]), 'stddev'),
      ('stddev broadcasted scale', ([0., 1., -0.5], 0.8), 'stddev'),
      ('mode', ([0., 1., -0.5], [0.5, 1., 1.5]), 'mode'),
      ('mode broadcasted loc', (0.5, [0.5, 1., 1.5]), 'mode'),
      ('mode broadcasted scale', ([0., 1., -0.5], 0.8), 'mode'),
  )
  def test_method(self, distr_params, function_string):
    distr_params = (np.asarray(distr_params[0], dtype=np.float32),
                    np.asarray(distr_params[1], dtype=np.float32))
    super()._test_attribute(
        attribute_string=function_string,
        dist_args=distr_params,
        assertion_fn=self.assertion_fn)

  @chex.all_variants(with_pmap=False)
  @parameterized.named_parameters(
      ('no broadcast', ([0., 1., -0.5], [0.5, 1., 1.5])),
      ('broadcasted loc', (0.5, [0.5, 1., 1.5])),
      ('broadcasted scale', ([0., 1., -0.5], 0.8)),
  )
  def test_median(self, distr_params):
    distr_params = (np.asarray(distr_params[0], dtype=np.float32),
                    np.asarray(distr_params[1], dtype=np.float32))
    dist = self.distrax_cls(*distr_params)
    self.assertion_fn(self.variant(dist.median)(), dist._loc - dist._scale * jnp.log(jnp.log(2)))

  @chex.all_variants(with_pmap=False)
  @parameterized.named_parameters(
      ('kl distrax_to_distrax', 'kl_divergence', 'distrax_to_distrax'),
      ('kl distrax_to_tfp', 'kl_divergence', 'distrax_to_tfp'),
      ('kl tfp_to_distrax', 'kl_divergence', 'tfp_to_distrax'),
      ('cross-ent distrax_to_distrax', 'cross_entropy', 'distrax_to_distrax'),
      ('cross-ent distrax_to_tfp', 'cross_entropy', 'distrax_to_tfp'),
      ('cross-ent tfp_to_distrax', 'cross_entropy', 'tfp_to_distrax')
  )
  def test_with_two_distributions(self, function_string, mode_string):
    super()._test_with_two_distributions(
        attribute_string=function_string,
        mode_string=mode_string,
        dist1_kwargs={
            'loc': np.random.randn(4, 1, 2),
            'scale': np.array([[0.8, 0.2], [0.1, 1.2], [1.4, 3.1]]),
        },
        dist2_kwargs={
            'loc': np.random.randn(3, 2),
            'scale': 0.1 + np.random.rand(4, 1, 2),
        },
        assertion_fn=self.assertion_fn)

  def test_jitable(self):
    super()._test_jittable((0.1, 1.2))


if __name__ == '__main__':
  absltest.main()