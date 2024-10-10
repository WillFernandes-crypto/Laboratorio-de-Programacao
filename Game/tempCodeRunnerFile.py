if not player.is_dead:
            player.update()
            player.move(move_left, move_right)
            player.apply_gravity(ground_level)
            player.draw(screen)
        else:
            # Se o jogador está morto, atualiza a animação de morte
            player.update()
            player.draw(screen, ground_level)  # Passando o nível do solo para o método draw