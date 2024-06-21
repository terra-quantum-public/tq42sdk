from tq42.exceptions import InvalidInputCliError


def check_params(command, args):
    if command == "exp run create":
        if (
            args.algorithm is None
            or args.compute is None
            or args.parameters is None
            or args.exp is None
        ):
            example_command = "Example usage: tq42 exp run create --exp 98ccb1d2-a3d0-48c8-b172-022f6db9be01  --compute small --algorithm TETRA_OPT --parameters \"{'parameters': {'dimensionality':6,'maximal_rank' :1, 'points_number': 1, 'quantization' : True , 'tolerance':3.9997,  'grid': [1,2,3], 'upper_limits':[1,2,3,4,6,6], 'lower_limits': [0,0,0,0,0,0] , 'objective_function':'https://terraquantum.swiss', 'iteration_number': 1}, 'inputs': {}}\" \n"
            raise SystemExit(InvalidInputCliError(msg=example_command))

    elif command == "org set":
        if args.org is None:
            example_command = (
                "Example usage: tq42 org set 5bac0b60-48d0-45cd-bf0a-39505b058106 \n\n"
            )
            raise SystemExit(InvalidInputCliError(msg=example_command))

    elif command == "exp set-friendly-name":
        if args.name is None or args.exp is None or args.exp == "":
            example_command = 'Example usage: tq42 exp set-friendly-name "FRIENDLY_NAME" --exp="EXP_ID"\n'
            raise SystemExit(InvalidInputCliError(msg=example_command))

    elif command == "exp run list":
        if not args.exp:
            example_command = "Example usage: tq42 exp run list --exp 98ccb1d2-a3d0-48c8-b172-022f6db9be01\n"
            raise SystemExit(InvalidInputCliError(msg=example_command))

    elif command == "proj list":
        if args.proj is None:
            example_command = "Example usage: tq42 proj dataset list --proj 98ccb1d2-a3d0-48c8-b172-022f6db9be01\n"
            raise SystemExit(InvalidInputCliError(msg=example_command))

    elif command == "proj dataset create":
        if (
            args.proj is None
            or args.name is None
            or args.desc is None
            or args.url is None
            or args.sensitivity is None
        ):
            example_command = 'Example usage: tq42 proj dataset create --proj 98ccb1d2-a3d0-48c8-b172-022f6db9be01 --name "Example Dataset Name" --desc "Example Description"  --url "https://mydata.com/drive/my-drive" --sensitivity "confidential" \n'
            raise SystemExit(InvalidInputCliError(msg=example_command))

    elif command == "proj dataset list":
        if args.proj is None:
            example_command = "Example usage: tq42 proj dataset list --proj 98ccb1d2-a3d0-48c8-b172-022f6db9be01\n"
            raise SystemExit(InvalidInputCliError(msg=example_command))

    elif command == "proj dataset get":
        if args.dataset is None:
            example_command = "Example usage: tq42 proj dataset get 98ccb1d2-a3d0-48c8-b172-022f6db9be01\n"
            raise SystemExit(InvalidInputCliError(msg=example_command))

    elif command == "proj dataset export":
        if args.dataset is None or args.directory_path is None:
            example_command = "Example usage: tq42 proj dataset export 98ccb1d2-a3d0-48c8-b172-022f6db9be01 /Users/user1/Downloads\n"
            raise SystemExit(InvalidInputCliError(msg=example_command))
