import type { Meta, StoryObj } from '@storybook/react';

import { Text } from './Typography';

const meta = {
  title: 'Text',
  component: Text,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<typeof Text>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Paragraphs: Story = {
  args: {
    children:
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean dapibus vehicula tincidunt. Mauris vel dui purus. Vestibulum ultricies egestas scelerisque. Proin venenatis consequat pellentesque. Nunc porttitor vestibulum velit. Nunc nec eros sit amet nibh luctus mattis. Nulla facilisi. Aenean euismod purus mi, et tincidunt velit auctor vitae',
  },
};
