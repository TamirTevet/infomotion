import * as React from 'react';
import Container from '@mui/material/Container/Container'
import { styled } from '@mui/styles';

const Div = styled(Container)(({ theme }) => ({
    ...theme.typography.button,
    backgroundColor: theme.palette.background.paper,
    padding: theme.spacing(1),
}));

export default function Logo(props) {
    return <Div>{props.name}</Div>;
}