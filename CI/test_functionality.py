# Tests for wheel

import pytest
import ray
import xoscar as mo

from xoscar_ray.backends.ray.utils import process_placement_to_address


class MyActor(mo.Actor):
    def __init__(self):
        self.i = 0

    def add(self, j: int) -> int:
        self.i += j
        return self.i

    def get(self) -> int:
        return self.i

    async def add_from(self, ref: mo.ActorRefType["MyActor"]) -> int:
        self.i += await ref.get()
        return self.i


@pytest.mark.asyncio
async def test_basic_cases():
    ray.init(num_cpus=2)
    try:
        pg_name, n_process = "ray_cluster", 2
        pg = ray.util.placement_group(name=pg_name, bundles=[{"CPU": n_process}])
        ray.get(pg.ready())
        address = process_placement_to_address(pg_name, 0, process_index=0)

        await mo.create_actor_pool(address, n_process=2)
        ref1 = await mo.create_actor(
            MyActor,
            address=address,
        )
        ref2 = await mo.create_actor(
            MyActor,
            address=address,
        )
        assert await ref1.add(1) == 1
        assert await ref2.add(2) == 2
        assert await ref1.add_from(ref2) == 3
    finally:
        ray.shutdown()
