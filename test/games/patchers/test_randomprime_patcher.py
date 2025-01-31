import json
import os
from unittest.mock import MagicMock, ANY

import pytest

import randovania
from randovania.game_description.resources.pickup_entry import PickupModel, ConditionalResources
from randovania.game_description.resources.pickup_index import PickupIndex
from randovania.games.game import RandovaniaGame
from randovania.games.patchers.randomprime_patcher import RandomprimePatcher, prime1_pickup_details_to_patcher
from randovania.games.prime.patcher_file_lib import pickup_exporter
from randovania.interface_common.players_configuration import PlayersConfiguration
from randovania.layout.layout_description import LayoutDescription
from randovania.layout.prime1.prime_cosmetic_patches import PrimeCosmeticPatches


@pytest.mark.parametrize("other_player", [False, True])
def test_prime1_pickup_details_to_patcher_shiny_missile(prime1_resource_database, other_player: bool):
    # Setup
    rng = MagicMock()
    rng.randint.return_value = 0
    detail = pickup_exporter.ExportedPickupDetails(
        index=PickupIndex(15),
        scan_text="Your Missile Expansion. Provides 5 Missiles",
        hud_text=["Missile Expansion acquired!"],
        conditional_resources=[ConditionalResources(
            None, None, (
                (prime1_resource_database.get_item_by_name("Missile"), 6),
            ),
        )],
        conversion=[],
        model=PickupModel(RandovaniaGame.METROID_PRIME, "Missile"),
        other_player=other_player,
    )
    if other_player:
        shiny_stuff = {
            'model': 'Missile',
            'scanText': 'Your Missile Expansion. Provides 5 Missiles',
            'hudmemoText': 'Missile Expansion acquired!',
        }
    else:
        shiny_stuff = {
            'model': 'Shiny Missile',
            'scanText': 'Your Shiny Missile Expansion. Provides 5 Missiles',
            'hudmemoText': 'Shiny Missile Expansion acquired!',
        }

    # Run
    result = prime1_pickup_details_to_patcher(detail, False, rng)

    # Assert
    assert result == {
        'type': 'Missile',
        'curr_increase': 6, 'max_increase': 6,
        'respawn': False,
        **shiny_stuff,
    }


def test_create_patch_data(test_files_dir):
    # Setup
    file = test_files_dir.joinpath("log_files", "prime1_and_2_multi.rdvgame")
    description = LayoutDescription.from_file(file)
    patcher = RandomprimePatcher()
    players_config = PlayersConfiguration(0, {0: "Prime", 1: "Echoes"})
    cosmetic_patches = PrimeCosmeticPatches()

    # Run
    data = patcher.create_patch_data(description, players_config, cosmetic_patches)

    # Assert
    phendrana = {
        'transports': {
            'Phendrana Drifts North\x00(Phendrana Shorelines)': 'Tallon Overworld East\x00(Frigate Crash Site)',
            'Phendrana Drifts South\x00(Quarantine Cave)': 'Magmoor Caverns West\x00(Monitor Station)'},
        'rooms': {
            'Phendrana Shorelines': {
                'pickups': [
                    {
                        'type': 'Missile',
                        'model': 'Missile',
                        'scanText': 'Your Missile Expansion. Provides 5 Missiles',
                        'hudmemoText': 'Missile Expansion acquired!',
                        'curr_increase': 5, 'max_increase': 5,
                        'respawn': False},
                    {
                        'type': 'Unknown Item 1',
                        'model': 'Nothing',
                        'scanText': "Echoes's Light Ammo Expansion. Provides 20 Light Ammo and 1 Item Percentage",
                        'hudmemoText': 'Sent Light Ammo Expansion to Echoes!',
                        'curr_increase': 37, 'max_increase': 37,
                        'respawn': False}]},
            'Chozo Ice Temple': {
                'pickups': [
                    {
                        'type': 'Unknown Item 1',
                        'model': 'Energy Tank',
                        'scanText': "Echoes's Energy Tank",
                        'hudmemoText': 'Sent Energy Tank to Echoes!',
                        'curr_increase': 38, 'max_increase': 38,
                        'respawn': False}]},
            'Ice Ruins West': {
                'pickups': [
                    {
                        'type': 'Unknown Item 1',
                        'model': 'Missile',
                        'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                        'hudmemoText': 'Sent Missile Expansion to Echoes!',
                        'curr_increase': 39, 'max_increase': 39,
                        'respawn': False}]},
            'Ice Ruins East': {
                'pickups': [
                    {
                        'type': 'Missile',
                        'model': 'Missile',
                        'scanText': 'Your Missile Expansion. Provides 5 Missiles',
                        'hudmemoText': 'Missile Expansion acquired!',
                        'curr_increase': 5, 'max_increase': 5,
                        'respawn': False},
                    {
                        'type': 'Unknown Item 1',
                        'model': 'Missile',
                        'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                        'hudmemoText': 'Sent Missile Expansion to Echoes!',
                        'curr_increase': 41, 'max_increase': 41,
                        'respawn': False}]},
            'Chapel of the Elders': {
                'pickups': [
                    {
                        'type': 'Missile',
                        'model': 'Missile',
                        'scanText': 'Your Missile Expansion. Provides 5 Missiles',
                        'hudmemoText': 'Missile Expansion acquired!',
                        'curr_increase': 5, 'max_increase': 5,
                        'respawn': False}]},
            'Ruined Courtyard': {
                'pickups': [
                    {
                        'type': 'Missile',
                        'model': 'Missile',
                        'scanText': 'Your Missile Expansion. Provides 5 Missiles',
                        'hudmemoText': 'Missile Expansion acquired!',
                        'curr_increase': 5, 'max_increase': 5,
                        'respawn': False}]},
            'Phendrana Canyon': {
                'pickups': [
                    {
                        'type': 'Unknown Item 1',
                        'model': 'Energy Tank',
                        'scanText': "Echoes's Energy Tank",
                        'hudmemoText': 'Sent Energy Tank to Echoes!',
                        'curr_increase': 44, 'max_increase': 44,
                        'respawn': False}]},
            'Quarantine Cave': {
                'pickups': [
                    {
                        'type': 'Energy Tank',
                        'model': 'Energy Tank',
                        'scanText': 'Your Energy Tank',
                        'hudmemoText': 'Energy Tank acquired!',
                        'curr_increase': 1, 'max_increase': 1,
                        'respawn': False}]},
            'Research Lab Hydra': {
                'pickups': [
                    {
                        'type': 'Missile',
                        'model': 'Missile',
                        'scanText': 'Your Missile Expansion. Provides 5 Missiles',
                        'hudmemoText': 'Missile Expansion acquired!',
                        'curr_increase': 5, 'max_increase': 5,
                        'respawn': False}]},
            'Quarantine Monitor': {
                'pickups': [
                    {
                        'type': 'Unknown Item 1',
                        'model': 'Missile',
                        'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                        'hudmemoText': 'Sent Missile Expansion to Echoes!',
                        'curr_increase': 47, 'max_increase': 47,
                        'respawn': False}]},
            'Observatory': {
                'pickups': [
                    {
                        'type': 'Missile',
                        'model': 'Missile',
                        'scanText': 'Your Missile Expansion. Provides 5 Missiles',
                        'hudmemoText': 'Missile Expansion acquired!',
                        'curr_increase': 5, 'max_increase': 5,
                        'respawn': False}]},
            'Transport Access': {
                'pickups': [
                    {
                        'type': 'Missile',
                        'model': 'Missile',
                        'scanText': 'Your Missile Expansion. Provides 5 Missiles',
                        'hudmemoText': 'Missile Expansion acquired!',
                        'curr_increase': 5, 'max_increase': 5,
                        'respawn': False}]},
            'Control Tower': {
                'pickups': [
                    {
                        'type': 'Unknown Item 1',
                        'model': 'Missile',
                        'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                        'hudmemoText': 'Sent Missile Expansion to Echoes!',
                        'curr_increase': 50, 'max_increase': 50,
                        'respawn': False}]},
            'Research Core': {
                'pickups': [
                    {
                        'type': 'Energy Tank',
                        'model': 'Energy Tank',
                        'scanText': 'Your Energy Tank',
                        'hudmemoText': 'Energy Tank acquired!',
                        'curr_increase': 1, 'max_increase': 1,
                        'respawn': False}]},
            'Frost Cave': {
                'pickups': [
                    {
                        'type': 'Energy Tank',
                        'model': 'Energy Tank',
                        'scanText': 'Your Energy Tank',
                        'hudmemoText': 'Energy Tank acquired!',
                        'curr_increase': 1, 'max_increase': 1,
                        'respawn': False}]},
            'Research Lab Aether': {
                'pickups': [
                    {
                        'type': 'Unknown Item 1',
                        'model': 'Missile',
                        'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                        'hudmemoText': 'Sent Missile Expansion to Echoes!',
                        'curr_increase': 53, 'max_increase': 53,
                        'modalHudmemo': True,
                        'respawn': False},
                    {
                        'type': 'Unknown Item 1',
                        'model': 'Power Bomb Expansion',
                        'scanText': "Echoes's Power Bomb Expansion. Provides 1 Power Bomb and 1 Item Percentage",
                        'hudmemoText': 'Sent Power Bomb Expansion to Echoes!',
                        'curr_increase': 54, 'max_increase': 54, 'modalHudmemo': True,
                        'respawn': False}]},
            'Gravity Chamber': {
                'pickups': [
                    {
                        'type': 'Missile',
                        'model': 'Missile',
                        'scanText': 'Your Missile Expansion. Provides 5 Missiles',
                        'hudmemoText': 'Missile Expansion acquired!',
                        'curr_increase': 5, 'max_increase': 5,
                        'respawn': False},
                    {
                        'type': 'Unknown Item 1',
                        'model': 'Missile',
                        'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                        'hudmemoText': 'Sent Missile Expansion to Echoes!',
                        'curr_increase': 56, 'max_increase': 56,
                        'respawn': False}]},
            'Storage Cave': {
                'pickups': [
                    {
                        'type': 'Missile',
                        'model': 'Missile',
                        'scanText': 'Your Missile Expansion. Provides 5 Missiles',
                        'hudmemoText': 'Missile Expansion acquired!',
                        'curr_increase': 5, 'max_increase': 5,
                        'respawn': False}]},
            'Security Cave': {
                'pickups': [
                    {
                        'type': 'Unknown Item 1',
                        'model': 'Missile',
                        'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                        'hudmemoText': 'Sent Missile Expansion to Echoes!',
                        'curr_increase': 58, 'max_increase': 58,
                        'respawn': False}]}}}
    magmoor = {
        'transports': {
            'Magmoor Caverns North\x00(Lava Lake)': 'Tallon Overworld West\x00(Root Cave)',
            'Magmoor Caverns West\x00(Monitor Station)': 'Phendrana Drifts South\x00(Quarantine Cave)',
            'Magmoor Caverns East\x00(Twin Fires)': 'Phazon Mines East\x00(Main Quarry)',
            'Magmoor Caverns South\x00(Magmoor Workstation, Debris)': 'Chozo Ruins South\x00(Reflecting Pool, Far End)',
            'Magmoor Caverns South\x00(Magmoor Workstation, Save Station)': 'Phazon Mines West\x00(Phazon Processing Center)'},
        'rooms': {
            'Lava Lake': {
                'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Morph Ball Bomb', 'scanText': "Echoes's Morph Ball Bomb",
                     'hudmemoText': 'Sent Morph Ball Bomb to Echoes!', 'curr_increase': 91, 'max_increase': 91,
                     'respawn': False}]},
            'Triclops Pit': {
                'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Power Bomb Expansion',
                     'scanText': "Echoes's Power Bomb Expansion. Provides 1 Power Bomb and 1 Item Percentage",
                     'hudmemoText': 'Sent Power Bomb Expansion to Echoes!',
                     'curr_increase': 92, 'max_increase': 92, 'respawn': False}]},
            'Storage Cavern': {
                'pickups': [
                    {'type': 'Energy Tank', 'model': 'Energy Tank',
                     'scanText': 'Your Energy Tank',
                     'hudmemoText': 'Energy Tank acquired!',
                     'curr_increase': 1, 'max_increase': 1, 'respawn': False}]},
            'Transport Tunnel A': {
                'pickups': [{'type': 'Missile', 'model': 'Missile',
                             'scanText': 'Your Missile Expansion. Provides 5 Missiles',
                             'hudmemoText': 'Missile Expansion acquired!',
                             'curr_increase': 5, 'max_increase': 5, 'respawn': False}]},
            'Warrior Shrine': {
                'pickups': [{'type': 'Unknown Item 1', 'model': 'Nothing',
                             'scanText': "Echoes's Light Ammo Expansion. Provides 20 Light Ammo and 1 Item Percentage",
                             'hudmemoText': 'Sent Light Ammo Expansion to Echoes!',
                             'curr_increase': 95, 'max_increase': 95, 'respawn': False}]},
            'Shore Tunnel': {
                'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Nothing',
                     'scanText': "Echoes's Dark Ammo Expansion. Provides 20 Dark Ammo and 1 Item Percentage",
                     'hudmemoText': 'Sent Dark Ammo Expansion to Echoes!',
                     'curr_increase': 96, 'max_increase': 96, 'respawn': False}]},
            'Fiery Shores': {
                'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Missile',
                     'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                     'hudmemoText': 'Sent Missile Expansion to Echoes!', 'curr_increase': 97, 'max_increase': 97,
                     'respawn': False},
                    {'type': 'Energy Tank', 'model': 'Energy Tank',
                     'scanText': 'Your Energy Tank',
                     'hudmemoText': 'Energy Tank acquired!', 'curr_increase': 1, 'max_increase': 1,
                     'respawn': False}
                ]},
            'Plasma Processing': {
                'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Missile',
                     'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                     'hudmemoText': 'Sent Missile Expansion to Echoes!', 'curr_increase': 99, 'max_increase': 99,
                     'respawn': False}
                ]},
            'Magmoor Workstation': {
                'pickups': [
                    {'type': 'Missile', 'model': 'Missile',
                     'scanText': 'Your Missile Expansion. Provides 5 Missiles',
                     'hudmemoText': 'Missile Expansion acquired!', 'curr_increase': 5, 'max_increase': 5,
                     'respawn': False}
                ]
            }
        }}
    mines = {
        'transports': {
            'Phazon Mines East\x00(Main Quarry)': 'Magmoor Caverns East\x00(Twin Fires)',
            'Phazon Mines West\x00(Phazon Processing Center)': 'Magmoor Caverns South\x00(Magmoor Workstation, Save Station)'},
        'rooms': {
            'Main Quarry': {
                'pickups': [
                    {
                        'type': 'Missile', 'model': 'Missile',
                        'scanText': 'Your Missile Expansion. Provides 5 Missiles',
                        'hudmemoText': 'Missile Expansion acquired!', 'curr_increase': 5, 'max_increase': 5,
                        'respawn': False}]},
            'Security Access A': {
                'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Energy Tank',
                     'scanText': "Echoes's Energy Tank",
                     'hudmemoText': 'Sent Energy Tank to Echoes!', 'curr_increase': 75, 'max_increase': 75,
                     'respawn': False}]},
            'Storage Depot B': {
                'pickups': [
                    {'type': 'Energy Tank', 'model': 'Energy Tank',
                     'scanText': 'Your Energy Tank',
                     'hudmemoText': 'Energy Tank acquired!', 'curr_increase': 1, 'max_increase': 1,
                     'respawn': False}]},
            'Storage Depot A': {
                'pickups': [
                    {'type': 'Spider Ball', 'model': 'Spider Ball',
                     'scanText': 'Your Spider Ball',
                     'hudmemoText': 'Spider Ball acquired!', 'curr_increase': 1, 'max_increase': 1,
                     'respawn': False}]},
            'Elite Research': {
                'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Nothing',
                     'scanText': "Echoes's Sonic Boom",
                     'hudmemoText': 'Sent Sonic Boom to Echoes!',
                     'curr_increase': 78, 'max_increase': 78, 'respawn': False},
                    {'type': 'Nothing', 'model': 'Nothing',
                     'scanText': 'Your Nothing',
                     'hudmemoText': 'Nothing acquired!',
                     'curr_increase': 0, 'max_increase': 0, 'respawn': False}
                ]},
            'Elite Control Access': {
                'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Missile',
                     'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                     'hudmemoText': 'Sent Missile Expansion to Echoes!',
                     'curr_increase': 80, 'max_increase': 80, 'respawn': False}
                ]},
            'Ventilation Shaft': {
                'pickups': [
                    {'type': 'Missile', 'model': 'Missile',
                     'scanText': 'Your Missile Expansion. Provides 5 Missiles',
                     'hudmemoText': 'Missile Expansion acquired!',
                     'curr_increase': 5, 'max_increase': 5, 'respawn': False}
                ]},
            'Phazon Processing Center': {
                'pickups': [
                    {'type': 'Power Bomb', 'model': 'Power Bomb Expansion',
                     'scanText': 'Your Power Bomb Expansion. Provides 1 Power Bomb',
                     'hudmemoText': 'Power Bomb Expansion acquired!',
                     'curr_increase': 1, 'max_increase': 1, 'respawn': False}]},
            'Processing Center Access': {
                'pickups': [
                    {'type': 'Missile', 'model': 'Missile',
                     'scanText': 'Your Missile Expansion. Provides 5 Missiles',
                     'hudmemoText': 'Missile Expansion acquired!',
                     'curr_increase': 5, 'max_increase': 5, 'respawn': False}]},
            'Elite Quarters': {
                'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Nothing',
                     'scanText': "Echoes's Light Ammo Expansion. Provides 20 Light Ammo and 1 Item Percentage",
                     'hudmemoText': 'Sent Light Ammo Expansion to Echoes!',
                     'curr_increase': 84, 'max_increase': 84, 'respawn': False}]},
            'Central Dynamo': {
                'pickups': [
                    {'type': 'Energy Tank', 'model': 'Energy Tank',
                     'scanText': 'Your Energy Tank',
                     'hudmemoText': 'Energy Tank acquired!', 'curr_increase': 1, 'max_increase': 1,
                     'respawn': False}]},
            'Metroid Quarantine B': {
                'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Nothing',
                     'scanText': "Echoes's Darkburst",
                     'hudmemoText': 'Sent Darkburst to Echoes!',
                     'curr_increase': 86, 'max_increase': 86, 'respawn': False}
                ]},
            'Metroid Quarantine A': {
                'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Missile',
                     'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                     'hudmemoText': 'Sent Missile Expansion to Echoes!',
                     'curr_increase': 87, 'max_increase': 87, 'respawn': False}]},
            'Fungal Hall B': {
                'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Nothing',
                     'scanText': "Echoes's Light Ammo Expansion. Provides 20 Light Ammo and 1 Item Percentage",
                     'hudmemoText': 'Sent Light Ammo Expansion to Echoes!',
                     'curr_increase': 88, 'max_increase': 88, 'respawn': False}]},
            'Phazon Mining Tunnel': {
                'pickups': [
                    {'type': 'Missile', 'model': 'Missile',
                     'scanText': 'Your Missile Expansion. Provides 5 Missiles',
                     'hudmemoText': 'Missile Expansion acquired!',
                     'curr_increase': 5, 'max_increase': 5, 'respawn': False}
                ]},
            'Fungal Hall Access': {
                'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Energy Tank',
                     'scanText': "Echoes's Energy Tank",
                     'hudmemoText': 'Sent Energy Tank to Echoes!',
                     'curr_increase': 90, 'max_increase': 90, 'respawn': False}]}}}
    overworld = {
        'transports': {
            'Artifact Temple': 'Crater Entry Point',
            'Tallon Overworld North\x00(Tallon Canyon)': 'Chozo Ruins East\x00(Reflecting Pool, Save Station)',
            'Tallon Overworld East\x00(Frigate Crash Site)': 'Phendrana Drifts North\x00(Phendrana Shorelines)',
            'Tallon Overworld West\x00(Root Cave)': 'Magmoor Caverns North\x00(Lava Lake)',
            'Tallon Overworld South\x00(Great Tree Hall, Upper)': 'Chozo Ruins West\x00(Main Plaza)',
            'Tallon Overworld South\x00(Great Tree Hall, Lower)': 'Chozo Ruins North\x00(Sun Tower)'},
        'rooms': {'Landing Site': {'pickups': [
            {'type': 'Varia Suit', 'model': 'Varia Suit',
             'scanText': 'Your Varia Suit',
             'hudmemoText': 'Varia Suit acquired!', 'curr_increase': 1, 'max_increase': 1,
             'respawn': False}]}, 'Alcove': {'pickups': [
            {'type': 'X-Ray Visor', 'model': 'X-Ray Visor',
             'scanText': 'Your X-Ray Visor',
             'hudmemoText': 'X-Ray Visor acquired!', 'curr_increase': 1, 'max_increase': 1,
             'respawn': False}]}, 'Frigate Crash Site': {'pickups': [
            {'type': 'Unknown Item 1', 'model': 'Nothing',
             'scanText': "Echoes's Emerald Translator",
             'hudmemoText': 'Sent Emerald Translator to Echoes!',
             'curr_increase': 61, 'max_increase': 61, 'respawn': False}]}, 'Overgrown Cavern': {
            'pickups': [{'type': 'Missile', 'model': 'Missile',
                         'scanText': 'Your Missile Expansion. Provides 5 Missiles',
                         'hudmemoText': 'Missile Expansion acquired!',
                         'curr_increase': 5, 'max_increase': 5, 'respawn': False}]}, 'Root Cave': {
            'pickups': [{'type': 'Plasma Beam', 'model': 'Plasma Beam',
                         'scanText': 'Your Plasma Beam',
                         'hudmemoText': 'Plasma Beam acquired!',
                         'curr_increase': 1, 'max_increase': 1, 'respawn': False}]},
            'Artifact Temple': {'pickups': [
                {'type': 'Unknown Item 1', 'model': 'Nothing',
                 'scanText': "Echoes's Violet Translator",
                 'hudmemoText': 'Sent Violet Translator to Echoes!',
                 'curr_increase': 64, 'max_increase': 64, 'respawn': False, 'modalHudmemo': True
                 }]},
            'Transport Tunnel B': {'pickups': [
                {'type': 'Artifact of Wild',
                 'model': 'Artifact of Wild',
                 'scanText': 'Your Artifact of Wild',
                 'hudmemoText': 'Artifact of Wild acquired!',
                 'curr_increase': 1, 'max_increase': 1, 'respawn': False}]},
            'Arbor Chamber': {'pickups': [
                {'type': 'Unknown Item 1', 'model': 'Nothing',
                 'scanText': "Echoes's Screw Attack",
                 'hudmemoText': 'Sent Screw Attack to Echoes!',
                 'curr_increase': 66, 'max_increase': 66, 'respawn': False}]},
            'Cargo Freight Lift to Deck Gamma': {'pickups': [
                {'type': 'Phazon Suit', 'model': 'Phazon Suit',
                 'scanText': 'Your Phazon Suit',
                 'hudmemoText': 'Phazon Suit acquired!',
                 'curr_increase': 1, 'max_increase': 1, 'respawn': False}]},
            'Biohazard Containment': {'pickups': [
                {'type': 'Unknown Item 1', 'model': 'Nothing',
                 'scanText': "Echoes's Dark Ammo Expansion. Provides 20 Dark Ammo and 1 Item Percentage",
                 'hudmemoText': 'Sent Dark Ammo Expansion to Echoes!',
                 'curr_increase': 68, 'max_increase': 68, 'respawn': False}]},
            'Hydro Access Tunnel': {'pickups': [
                {'type': 'Missile', 'model': 'Missile',
                 'scanText': 'Your Missile Expansion. Provides 5 Missiles',
                 'hudmemoText': 'Missile Expansion acquired!',
                 'curr_increase': 5, 'max_increase': 5, 'respawn': False}]},
            'Great Tree Chamber': {'pickups': [
                {'type': 'Energy Tank', 'model': 'Energy Tank',
                 'scanText': 'Your Energy Tank',
                 'hudmemoText': 'Energy Tank acquired!',
                 'curr_increase': 1, 'max_increase': 1, 'respawn': False}]},
            'Life Grove Tunnel': {'pickups': [
                {'type': 'Unknown Item 1', 'model': 'Nothing',
                 'scanText': "Echoes's Light Ammo Expansion. Provides 20 Light Ammo and 1 Item Percentage",
                 'hudmemoText': 'Sent Light Ammo Expansion to Echoes!',
                 'curr_increase': 71, 'max_increase': 71, 'respawn': False}]}, 'Life Grove': {
                'pickups': [{'type': 'Boost Ball', 'model': 'Boost Ball',
                             'scanText': 'Your Boost Ball',
                             'hudmemoText': 'Boost Ball acquired!',
                             'curr_increase': 1, 'max_increase': 1, 'respawn': False},
                            {'type': 'Missile', 'model': 'Missile',
                             'scanText': 'Your Missile Expansion. Provides 5 Missiles',
                             'hudmemoText': 'Missile Expansion acquired!',
                             'curr_increase': 5, 'max_increase': 5, 'respawn': False}]}}}
    chozo = {
        'transports': {
            'Chozo Ruins West\x00(Main Plaza)': 'Tallon Overworld South\x00(Great Tree Hall, Upper)',
            'Chozo Ruins North\x00(Sun Tower)': 'Tallon Overworld South\x00(Great Tree Hall, Lower)',
            'Chozo Ruins East\x00(Reflecting Pool, Save Station)': 'Tallon Overworld North\x00(Tallon Canyon)',
            'Chozo Ruins South\x00(Reflecting Pool, Far End)': 'Magmoor Caverns South\x00(Magmoor Workstation, Debris)'
        },
        'rooms': {
            'Main Plaza': {
                'pickups': [
                    {'type': 'Power Bomb', 'model': 'Power Bomb Expansion',
                     'scanText': 'Your Power Bomb Expansion. Provides 1 Power Bomb',
                     'hudmemoText': 'Power Bomb Expansion acquired!', 'curr_increase': 1, 'max_increase': 1,
                     'respawn': False},
                    {'type': 'Power Bomb', 'model': 'Power Bomb',
                     'scanText': 'Your Power Bomb',
                     'hudmemoText': 'Power Bomb acquired!', 'curr_increase': 4, 'max_increase': 4,
                     'respawn': False},
                    {'type': 'Missile', 'model': 'Missile',
                     'scanText': 'Your Missile Expansion. Provides 5 Missiles',
                     'hudmemoText': 'Missile Expansion acquired!',
                     'curr_increase': 5, 'max_increase': 5, 'respawn': False},
                    {'type': 'Missile', 'model': 'Missile',
                     'scanText': 'Your Missile Expansion. Provides 5 Missiles',
                     'hudmemoText': 'Missile Expansion acquired!',
                     'curr_increase': 5, 'max_increase': 5, 'respawn': False}
                ]},
            'Ruined Fountain': {
                'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Missile',
                     'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                     'hudmemoText': 'Sent Missile Expansion to Echoes!',
                     'curr_increase': 5, 'max_increase': 5, 'respawn': False}]
            },
            'Ruined Shrine': {
                'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Nothing',
                     'scanText': "Echoes's Dark Ammo Expansion. Provides 20 Dark Ammo and 1 Item Percentage",
                     'hudmemoText': 'Sent Dark Ammo Expansion to Echoes!',
                     'curr_increase': 6, 'max_increase': 6, 'respawn': False, 'modalHudmemo': True},
                    {'type': 'Unknown Item 1', 'model': 'Power Bomb Expansion',
                     'scanText': "Echoes's Power Bomb Expansion. Provides 1 Power Bomb and 1 Item Percentage",
                     'hudmemoText': 'Sent Power Bomb Expansion to Echoes!',
                     'curr_increase': 7, 'max_increase': 7, 'respawn': False, 'modalHudmemo': True},
                    {'type': 'Unknown Item 1', 'model': 'Missile',
                     'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                     'hudmemoText': 'Sent Missile Expansion to Echoes!',
                     'curr_increase': 8, 'max_increase': 8, 'respawn': False, 'modalHudmemo': True}]
            },
            'Vault': {
                'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Missile',
                     'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                     'hudmemoText': 'Sent Missile Expansion to Echoes!',
                     'curr_increase': 9, 'max_increase': 9, 'respawn': False}
                ]},
            'Training Chamber': {
                'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Energy Tank',
                     'scanText': "Echoes's Energy Tank",
                     'hudmemoText': 'Sent Energy Tank to Echoes!',
                     'curr_increase': 10, 'max_increase': 10, 'respawn': False}]},
            'Ruined Nursery': {
                'pickups': [
                    {'type': 'Missile', 'model': 'Missile',
                     'scanText': 'Your Missile Expansion. Provides 5 Missiles',
                     'hudmemoText': 'Missile Expansion acquired!',
                     'curr_increase': 5, 'max_increase': 5, 'respawn': False}
                ]},
            'Training Chamber Access': {
                'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Missile',
                     'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                     'hudmemoText': 'Sent Missile Expansion to Echoes!',
                     'curr_increase': 12, 'max_increase': 12, 'respawn': False}]},
            'Magma Pool': {
                'pickups': [
                    {'type': 'Energy Tank', 'model': 'Energy Tank',
                     'scanText': 'Your Energy Tank',
                     'hudmemoText': 'Energy Tank acquired!',
                     'curr_increase': 1, 'max_increase': 1, 'respawn': False}]},
            'Tower of Light': {
                'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Missile',
                     'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                     'hudmemoText': 'Sent Missile Expansion to Echoes!',
                     'curr_increase': 14, 'max_increase': 14, 'respawn': False
                     }]},
            'Tower Chamber': {
                'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Power Bomb Expansion',
                     'scanText': "Echoes's Power Bomb Expansion. Provides 1 Power Bomb and 1 Item Percentage",
                     'hudmemoText': 'Sent Power Bomb Expansion to Echoes!',
                     'curr_increase': 15, 'max_increase': 15, 'respawn': False}]},
            'Ruined Gallery': {
                'pickups': [
                    {'type': 'Missile', 'model': 'Missile',
                     'scanText': 'Your Missile Expansion. Provides 5 Missiles',
                     'hudmemoText': 'Missile Expansion acquired!',
                     'curr_increase': 5, 'max_increase': 5, 'respawn': False},
                    {'type': 'Unknown Item 1', 'model': 'Missile',
                     'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                     'hudmemoText': 'Sent Missile Expansion to Echoes!',
                     'curr_increase': 17, 'max_increase': 17, 'respawn': False}
                ]},
            'Transport Access North': {
                'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Missile',
                     'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                     'hudmemoText': 'Sent Missile Expansion to Echoes!',
                     'curr_increase': 18, 'max_increase': 18, 'respawn': False, 'modalHudmemo': True
                     }]},
            'Gathering Hall': {
                'pickups': [
                    {'type': 'Missile', 'model': 'Missile',
                     'scanText': 'Your Missile Expansion. Provides 5 Missiles',
                     'hudmemoText': 'Missile Expansion acquired!',
                     'curr_increase': 5, 'max_increase': 5, 'respawn': False}]},
            'Hive Totem': {
                'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Nothing',
                     'scanText': "Echoes's Dark Ammo Expansion. Provides 20 Dark Ammo and 1 Item Percentage",
                     'hudmemoText': 'Sent Dark Ammo Expansion to Echoes!',
                     'curr_increase': 20, 'max_increase': 20, 'respawn': False, 'modalHudmemo': True,
                     }]},
            'Sunchamber': {
                'pickups': [
                    {'type': 'Missile', 'model': 'Missile',
                     'scanText': 'Your Missile Expansion. Provides 5 Missiles',
                     'hudmemoText': 'Missile Expansion acquired!',
                     'curr_increase': 5, 'max_increase': 5, 'respawn': False},
                    {'type': 'Wavebuster', 'model': 'Wavebuster',
                     'scanText': 'Your Wavebuster',
                     'hudmemoText': 'Wavebuster acquired!',
                     'curr_increase': 1, 'max_increase': 1, 'respawn': False}]},
            'Watery Hall Access': {
                'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Nothing',
                     'scanText': "Echoes's Dark Ammo Expansion. Provides 20 Dark Ammo and 1 Item Percentage",
                     'hudmemoText': 'Sent Dark Ammo Expansion to Echoes!',
                     'curr_increase': 23, 'max_increase': 23, 'respawn': False}]},
            'Watery Hall': {
                'pickups': [
                    {'type': 'Energy Tank', 'model': 'Energy Tank',
                     'scanText': 'Your Energy Tank',
                     'hudmemoText': 'Energy Tank acquired!',
                     'curr_increase': 1, 'max_increase': 1, 'respawn': False},
                    {'type': 'Energy Tank', 'model': 'Energy Tank',
                     'scanText': 'Your Energy Tank',
                     'hudmemoText': 'Energy Tank acquired!',
                     'curr_increase': 1, 'max_increase': 1, 'respawn': False}]},
            'Dynamo': {
                'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Nothing',
                     'scanText': "Echoes's Dark Ammo Expansion. Provides 20 Dark Ammo and 1 Item Percentage",
                     'hudmemoText': 'Sent Dark Ammo Expansion to Echoes!',
                     'curr_increase': 26, 'max_increase': 26, 'respawn': False},
                    {'type': 'Missile', 'model': 'Missile',
                     'scanText': 'Your Missile Expansion. Provides 5 Missiles',
                     'hudmemoText': 'Missile Expansion acquired!',
                     'curr_increase': 5, 'max_increase': 5, 'respawn': False}]
            },
            'Burn Dome': {
                'pickups': [
                    {'type': 'Missile', 'model': 'Missile',
                     'scanText': 'Your Missile Expansion. Provides 5 Missiles',
                     'hudmemoText': 'Missile Expansion acquired!',
                     'curr_increase': 5, 'max_increase': 5, 'respawn': False},
                    {'type': 'Unknown Item 1', 'model': 'Energy Tank',
                     'scanText': "Echoes's Energy Tank",
                     'hudmemoText': 'Sent Energy Tank to Echoes!',
                     'curr_increase': 29, 'max_increase': 29, 'respawn': False}]},
            'Furnace': {
                'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Nothing',
                     'scanText': "Echoes's Light Ammo Expansion. Provides 20 Light Ammo and 1 Item Percentage",
                     'hudmemoText': 'Sent Light Ammo Expansion to Echoes!',
                     'curr_increase': 30, 'max_increase': 30, 'respawn': False},
                    {'type': 'Unknown Item 1', 'model': 'Energy Tank',
                     'scanText': "Echoes's Energy Tank",
                     'hudmemoText': 'Sent Energy Tank to Echoes!',
                     'curr_increase': 31, 'max_increase': 31, 'respawn': False}]},
            'Hall of the Elders': {
                'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Missile',
                     'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                     'hudmemoText': 'Sent Missile Expansion to Echoes!',
                     'curr_increase': 32, 'max_increase': 32, 'respawn': False}]}, 'Crossway': {
                'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Nothing',
                     'scanText': "Echoes's Dark Ammo Expansion. Provides 20 Dark Ammo and 1 Item Percentage",
                     'hudmemoText': 'Sent Dark Ammo Expansion to Echoes!',
                     'curr_increase': 33, 'max_increase': 33, 'respawn': False}]},
            'Elder Chamber': {'pickups': [
                {'type': 'Unknown Item 1', 'model': 'Energy Tank',
                 'scanText': "Echoes's Energy Tank",
                 'hudmemoText': 'Sent Energy Tank to Echoes!',
                 'curr_increase': 34, 'max_increase': 34, 'respawn': False}]},
            'Antechamber': {
                'pickups': [{
                    'type': 'Unknown Item 1',
                    'model': 'Power Bomb Expansion',
                    'scanText': "Echoes's Power Bomb Expansion. Provides 1 Power Bomb and 1 Item Percentage",
                    'hudmemoText': 'Sent Power Bomb Expansion to Echoes!',
                    'curr_increase': 35, 'max_increase': 35, 'respawn': False
                }]}}}

    expected_data = {
        'seed': 1499122484,
        'hasSpoiler': True,
        'preferences': {
            'artifactHintBehavior': None,
            'automaticCrashScreen': True,
            'mapDefaultState': 'default',
            'obfuscateItems': False,
            'qolCosmetic': True,
            'qolGameBreaking': True,
            'qolCutscenes': 'original',
            'qolPickupScans': False,
            'quickplay': False,
            'quiet': False,
            'trilogyDiscPath': None,
        },
        'gameConfig': {
            'artifactHints': {
                'Artifact of Chozo': '&push;&main-color=#c300ff;Artifact of Chozo&pop; is located in '
                                     "&push;&main-color=#d4cc33;Echoes&pop;'s "
                                     "&push;&main-color=#89a1ff;Dark Agon Wastes - Ing Cache 1&pop;.",
                'Artifact of Elder': '&push;&main-color=#c300ff;Artifact of Elder&pop; is located in '
                                     "&push;&main-color=#d4cc33;Echoes&pop;'s "
                                     '&push;&main-color=#89a1ff;Agon Wastes - Sand Cache&pop;.',
                'Artifact of Lifegiver': '&push;&main-color=#c300ff;Artifact of Lifegiver&pop; is located in '
                                         "&push;&main-color=#d4cc33;Echoes&pop;'s "
                                         '&push;&main-color=#89a1ff;Temple Grounds - Storage Cavern B&pop;.',
                'Artifact of Nature': '&push;&main-color=#c300ff;Artifact of Nature&pop; is located in '
                                      "&push;&main-color=#d4cc33;Echoes&pop;'s "
                                      '&push;&main-color=#89a1ff;Sanctuary Fortress - Hall of Combat Mastery&pop;.',
                'Artifact of Newborn': '&push;&main-color=#c300ff;Artifact of Newborn&pop; is located in '
                                       "&push;&main-color=#d4cc33;Echoes&pop;'s "
                                       '&push;&main-color=#89a1ff;Great Temple - Transport A Access&pop;.',
                'Artifact of Spirit': '&push;&main-color=#c300ff;Artifact of Spirit&pop; is located in '
                                      "&push;&main-color=#d4cc33;Echoes&pop;'s "
                                      '&push;&main-color=#89a1ff;Temple Grounds - Transport to Agon Wastes&pop;.',
                'Artifact of Strength': '&push;&main-color=#c300ff;Artifact of Strength&pop; is located in '
                                        "&push;&main-color=#d4cc33;Echoes&pop;'s "
                                        '&push;&main-color=#89a1ff;Agon Wastes - Storage D&pop;.',
                'Artifact of Sun': '&push;&main-color=#c300ff;Artifact of Sun&pop; has no need to be located.',
                'Artifact of Truth': '&push;&main-color=#c300ff;Artifact of Truth&pop; is located in '
                                     "&push;&main-color=#d4cc33;Echoes&pop;'s "
                                     '&push;&main-color=#89a1ff;Agon Wastes - Mining Station Access&pop;.',
                'Artifact of Warrior': '&push;&main-color=#c300ff;Artifact of Warrior&pop; is located in '
                                       "&push;&main-color=#d4cc33;Echoes&pop;'s "
                                       '&push;&main-color=#89a1ff;Agon Wastes - Portal Access A&pop;.',
                'Artifact of Wild': '&push;&main-color=#c300ff;Artifact of Wild&pop; is located in '
                                    "&push;&main-color=#d4cc33;Prime&pop;'s "
                                    '&push;&main-color=#89a1ff;Tallon Overworld - Transport Tunnel B&pop;.',
                'Artifact of World': '&push;&main-color=#c300ff;Artifact of World&pop; is located in '
                                     "&push;&main-color=#d4cc33;Echoes&pop;'s "
                                     '&push;&main-color=#89a1ff;Ing Hive - Culling Chamber&pop;.'
            },

            'artifactTempleLayerOverrides': {
                'Artifact of Chozo': True,
                'Artifact of Elder': True,
                'Artifact of Lifegiver': True,
                'Artifact of Nature': True,
                'Artifact of Newborn': True,
                'Artifact of Spirit': True,
                'Artifact of Strength': True,
                'Artifact of Sun': False,
                'Artifact of Truth': True,
                'Artifact of Warrior': True,
                'Artifact of Wild': True,
                'Artifact of World': True,
            },
            'autoEnabledElevators': False,
            'multiworldDolPatches': True,
            'creditsString': (
                "&push;&font=C29C51F1;&main-color=#89D6FF;Major Item Locations&pop;"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;Charge Beam&pop;\n"
                "&push;&main-color=#d4cc33;Echoes&pop;'s Sanctuary Fortress - Sanctuary Energy Controller"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;Wave Beam&pop;\n"
                "&push;&main-color=#d4cc33;Echoes&pop;'s Torvus Bog - Great Bridge"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;Ice Beam&pop;\n"
                "&push;&main-color=#d4cc33;Echoes&pop;'s Temple Grounds - Temple Assembly Site"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;Plasma Beam&pop;\n"
                "&push;&main-color=#d4cc33;Prime&pop;'s Tallon Overworld - Root Cave"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;Grapple Beam&pop;\n"
                "&push;&main-color=#d4cc33;Echoes&pop;'s Dark Agon Wastes - Junction Site"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;Thermal Visor&pop;\n"
                "&push;&main-color=#d4cc33;Echoes&pop;'s Torvus Bog - Torvus Energy Controller"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;X-Ray Visor&pop;\n"
                "&push;&main-color=#d4cc33;Prime&pop;'s Tallon Overworld - Alcove"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;Boost Ball&pop;\n"
                "&push;&main-color=#d4cc33;Prime&pop;'s Tallon Overworld - Life Grove"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;Spider Ball&pop;\n"
                "&push;&main-color=#d4cc33;Prime&pop;'s Phazon Mines - Storage Depot A"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;Power Bomb&pop;\n"
                "&push;&main-color=#d4cc33;Prime&pop;'s Chozo Ruins - Main Plaza"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;Varia Suit&pop;\n"
                "&push;&main-color=#d4cc33;Prime&pop;'s Tallon Overworld - Landing Site"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;Gravity Suit&pop;\n"
                "&push;&main-color=#d4cc33;Echoes&pop;'s Great Temple - Transport B Access"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;Phazon Suit&pop;\n"
                "&push;&main-color=#d4cc33;Prime&pop;'s Tallon Overworld - Cargo Freight Lift to Deck Gamma"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;Super Missile&pop;\n"
                "&push;&main-color=#d4cc33;Echoes&pop;'s Temple Grounds - Windchamber Gateway"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;Wavebuster&pop;\n"
                "&push;&main-color=#d4cc33;Prime&pop;'s Chozo Ruins - Sunchamber"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;Ice Spreader&pop;\n"
                "&push;&main-color=#d4cc33;Echoes&pop;'s Agon Wastes - Sandcanyon"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;Flamethrower&pop;\n"
                "&push;&main-color=#d4cc33;Echoes&pop;'s Torvus Bog - Training Chamber"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;Artifact of Chozo&pop;\n"
                "&push;&main-color=#d4cc33;Echoes&pop;'s Dark Agon Wastes - Ing Cache 1"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;Artifact of Elder&pop;\n"
                "&push;&main-color=#d4cc33;Echoes&pop;'s Agon Wastes - Sand Cache"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;Artifact of Lifegiver&pop;\n"
                "&push;&main-color=#d4cc33;Echoes&pop;'s Temple Grounds - Storage Cavern B"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;Artifact of Nature&pop;\n"
                "&push;&main-color=#d4cc33;Echoes&pop;'s Sanctuary Fortress - Hall of Combat Mastery"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;Artifact of Newborn&pop;\n"
                "&push;&main-color=#d4cc33;Echoes&pop;'s Great Temple - Transport A Access"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;Artifact of Spirit&pop;\n"
                "&push;&main-color=#d4cc33;Echoes&pop;'s Temple Grounds - Transport to Agon Wastes"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;Artifact of Strength&pop;\n"
                "&push;&main-color=#d4cc33;Echoes&pop;'s Agon Wastes - Storage D"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;Artifact of Truth&pop;\n"
                "&push;&main-color=#d4cc33;Echoes&pop;'s Agon Wastes - Mining Station Access"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;Artifact of Warrior&pop;\n"
                "&push;&main-color=#d4cc33;Echoes&pop;'s Agon Wastes - Portal Access A"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;Artifact of Wild&pop;\n"
                "&push;&main-color=#d4cc33;Prime&pop;'s Tallon Overworld - Transport Tunnel B"

                "\n\n&push;&font=C29C51F1;&main-color=#33ffd6;Artifact of World&pop;\n"
                "&push;&main-color=#d4cc33;Echoes&pop;'s Ing Hive - Culling Chamber"
            ),
            'etankCapacity': 110,

            "mainPlazaDoor": True,
            "backwardsFrigate": True,
            "backwardsLabs": True,
            "backwardsUpperMines": True,
            "backwardsLowerMines": False,
            "phazonEliteWithoutDynamo": True,

            'gameBanner': {'description': 'Seed Hash: Caretaker Lumigek Skiff',
                           'gameName': 'Metroid Prime: Randomizer',
                           'gameNameFull': 'Metroid Prime: Randomizer - Z2OYS7HX'},
            'heatDamagePerSec': 10.0,
            'itemMaxCapacity': {'Unknown Item 1': 65536},
            'mainMenuMessage': f'Randovania v{randovania.VERSION}\nCaretaker Lumigek Skiff',
            'nonvariaHeatDamage': True,
            'staggeredSuitDamage': True,
            'startingItems': {
                'bombs': False,
                'boostBall': False,
                'combatVisor': True,
                'charge': False,
                'energyTanks': 0,
                'flamethrower': False,
                'grapple': False,
                'gravitySuit': False,
                'ice': False,
                'iceSpreader': False,
                'missiles': 5,
                'morphBall': True,
                'phazonSuit': False,
                'plasma': False,
                'powerBeam': True,
                'powerBombs': 0,
                'scanVisor': True,
                'spaceJump': True,
                'spiderBall': False,
                'superMissile': False,
                'thermalVisor': False,
                'variaSuit': False,
                'wave': False,
                'wavebuster': False,
                'xray': False,
            },
            'startingMemo': 'Artifact of Sun, 5 Missiles',
            'startingRoom': 'Tallon Overworld:Landing Site',
            'warpToStart': False,
        },
        "tweaks": {},
        'levelData': {
            'Impact Crater': {
                'rooms': {},
                'transports': {
                    'Crater Entry Point': 'Artifact Temple',
                },
            },
            'Phendrana Drifts': phendrana,
            'Frigate Orpheon': {'transports': {}, 'rooms': {}},
            'Magmoor Caverns': magmoor,
            'Phazon Mines': mines,
            'Tallon Overworld': overworld,
            'Chozo Ruins': chozo
        },
    }

    assert data == expected_data

def test_patch_game(mocker, tmp_path):
    mock_symbols_for_file: MagicMock = mocker.patch("py_randomprime.symbols_for_file", return_value={
        "UpdateHintState__13CStateManagerFf": 0x80044D38,
    })
    mock_patch_iso_raw: MagicMock = mocker.patch("py_randomprime.patch_iso_raw")
    patch_data = {"patch": "data", 'gameConfig': {}, 'hasSpoiler': True}
    game_files_path = MagicMock()
    progress_update = MagicMock()

    patcher = RandomprimePatcher()

    # Run
    patcher.patch_game(tmp_path.joinpath("input.iso"), tmp_path.joinpath("output.iso"),
                       patch_data, game_files_path, progress_update)

    # Assert
    expected = {
        "patch": "data",
        'gameConfig': {
            "updateHintStateReplacement": [
                148, 33, 255, 204, 124, 8, 2, 166, 144, 1, 0, 56, 191, 193, 0, 44, 124, 127, 27, 120, 136, 159, 0, 2,
                44, 4, 0, 0, 64, 130, 0, 24, 187, 193, 0, 44, 128, 1, 0, 56, 124, 8, 3, 166, 56, 33, 0, 52, 78,
                128, 0, 32, 56, 192, 0, 0, 152, 223, 0, 2, 63, 192, 128, 4, 99, 222, 77, 148, 56, 128, 1, 0, 124, 4,
                247, 172, 44, 4, 0, 0, 56, 132, 255, 224, 64, 130, 255, 244, 124, 0, 4, 172, 76, 0, 1, 44, 187,
                193, 0, 44, 128, 1, 0, 56, 124, 8, 3, 166, 56, 33, 0, 52, 78, 128, 0, 32
            ]
        },
        "inputIso": os.fspath(tmp_path.joinpath("input.iso")),
        "outputIso": os.fspath(tmp_path.joinpath("output.iso")),
    }
    mock_symbols_for_file.assert_called_once_with(tmp_path.joinpath("input.iso"))
    mock_patch_iso_raw.assert_called_once_with(json.dumps(expected, indent=4, separators=(',', ': ')), ANY)
